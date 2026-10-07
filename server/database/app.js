const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');

const app = express();
const port = 3030;

app.use(cors());
app.use(express.urlencoded({ extended: false }));
app.use(express.json());

const reviews_data = JSON.parse(
  fs.readFileSync('reviews.json', 'utf8')
);
const dealerships_data = JSON.parse(
  fs.readFileSync('dealerships.json', 'utf8')
);

const Reviews = require('./review');
const Dealerships = require('./dealership');

// Home
app.get('/', (req, res) => {
  res.send('Welcome to the Mongoose API');
});

// Get all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Get reviews for one dealership
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({
      dealership: req.params.id
    });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Get all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    const documents = await Dealerships.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Get dealerships in one state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const documents = await Dealerships.find({
      state: req.params.state
    });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Get one dealership by ID
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const documents = await Dealerships.find({
      id: req.params.id
    });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Insert a review
app.post(
  '/insert_review',
  express.raw({ type: '*/*' }),
  async (req, res) => {
    try {
      const data = Buffer.isBuffer(req.body)
        ? JSON.parse(req.body.toString('utf8'))
        : req.body;

      const latestReview = await Reviews.findOne().sort({ id: -1 });
      const new_id = latestReview ? latestReview.id + 1 : 1;

      const review = new Reviews({
        id: new_id,
        name: data.name,
        dealership: data.dealership,
        review: data.review,
        purchase: data.purchase,
        purchase_date: data.purchase_date,
        car_make: data.car_make,
        car_model: data.car_model,
        car_year: data.car_year
      });

      const savedReview = await review.save();
      res.json(savedReview);
    } catch (error) {
      console.error(error);
      const invalidData =
        error instanceof SyntaxError ||
        error instanceof TypeError ||
        error.name === 'ValidationError';

      res.status(invalidData ? 400 : 500).json({
        error: 'Error inserting review'
      });
    }
  }
);

// Connect to MongoDB, load initial data, then start the server
async function startServer() {
  try {
    await mongoose.connect('mongodb://mongo_db:27017/', {
      dbName: 'dealershipsDB'
    });

    if (await Reviews.countDocuments() === 0) {
      await Reviews.insertMany(reviews_data.reviews);
    }

    if (await Dealerships.countDocuments() === 0) {
      await Dealerships.insertMany(dealerships_data.dealerships);
    }

    app.listen(port, '0.0.0.0', () => {
      console.log(`Server is running on http://localhost:${port}`);
    });
  } catch (error) {
    console.error('Error starting server:', error);
    process.exit(1);
  }
}

startServer();