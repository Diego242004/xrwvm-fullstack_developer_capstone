import React, { useState } from "react";
import "./Register.css";
import user_icon from "../assets/person.png";
import email_icon from "../assets/email.png";
import password_icon from "../assets/password.png";
import close_icon from "../assets/close.png";

const Register = () => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");

  const register = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(window.location.origin + "/djangoapp/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userName, password, firstName, lastName, email }),
      });
      const json = await res.json();
      if (res.ok && json.status === "Authenticated") {
        sessionStorage.setItem("username", json.userName);
        window.location.href = window.location.origin;
      } else if (json.error === "Already Registered") {
        alert("The user with same username is already registered");
      } else {
        alert(json.error || "The user could not be registered.");
      }
    } catch (error) {
      alert("The user could not be registered. Please try again.");
    }
  };

  return (
    <div className="register_container" style={{ width: "50%", maxWidth: "600px" }}>
      <div className="header" style={{ display: "flex", justifyContent: "space-between" }}>
        <span className="text" style={{ flexGrow: 1 }}>SignUp</span>
        <a href="/" aria-label="Return to home">
          <img style={{ width: "1cm" }} src={close_icon} alt="" />
        </a>
      </div>
      <form onSubmit={register}>
        <div className="inputs">
          <div className="input">
            <img src={user_icon} className="img_icon" alt="" />
            <input type="text" name="username" placeholder="Username" aria-label="Username" autoComplete="username" className="input_field" required value={userName} onChange={(e) => setUserName(e.target.value)} />
          </div>
          <div className="input">
            <img src={user_icon} className="img_icon" alt="" />
            <input type="text" name="first_name" placeholder="First Name" aria-label="First Name" autoComplete="given-name" className="input_field" required value={firstName} onChange={(e) => setFirstName(e.target.value)} />
          </div>
          <div className="input">
            <img src={user_icon} className="img_icon" alt="" />
            <input type="text" name="last_name" placeholder="Last Name" aria-label="Last Name" autoComplete="family-name" className="input_field" required value={lastName} onChange={(e) => setLastName(e.target.value)} />
          </div>
          <div className="input">
            <img src={email_icon} className="img_icon" alt="" />
            <input type="email" name="email" placeholder="email" aria-label="Email" autoComplete="email" className="input_field" required value={email} onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div className="input">
            <img src={password_icon} className="img_icon" alt="" />
            <input type="password" name="psw" placeholder="Password" aria-label="Password" autoComplete="new-password" className="input_field" required value={password} onChange={(e) => setPassword(e.target.value)} />
          </div>
        </div>
        <div className="submit_panel">
          <input className="submit" type="submit" value="Register" />
        </div>
      </form>
    </div>
  );
};

export default Register;
