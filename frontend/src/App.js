import "./App.css";
import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom";
import HomeLayout from "./containers/HomeLayout";
import Login from "./containers/Login";

function App() {
  return (
    <div className="App">
      <Router>
        <div className="App">
          <Routes>
            <Route path="/" exact component={<HomeLayout />} />
            <Route path="/login" component={<Login />} />
          </Routes>
        </div>
      </Router>
    </div>
  );
}

export default App;
