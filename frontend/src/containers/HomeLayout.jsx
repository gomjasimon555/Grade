// import React, { useState } from "react";
// // import "./home.css";
// // import Loader from "../../components/Loader";
// import axios from "axios";

// const HomeLayout = () => {
//   const [input1, setInput1] = useState("");
//   const [input2, setInput2] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [grade_decisiontree, set_grade_decisiontree] = useState("");
//   const [grade_randomforest, set_grade_randomforest] = useState("");
//   const [plotUrl, setPlotUrl] = useState("");
//   console.log("plotUrl:", plotUrl);

//   const handleInputChange1 = (e) => {
//     setInput1(e.target.value);
//   };

//   const handleInputChange2 = (e) => {
//     setInput2(e.target.value);
//   };

//   const handleSubmit = (e) => {
//     setLoading(true);

//     e.preventDefault();
//     // console.log('Input 1:', input1);
//     // console.log('Input 2:', input2);
//     axios
//       .post("http://localhost:5000/viewgrade", { name: input2, symbol: input1 })
//       .then((response) => {
//         console.log(response.data);
//         setLoading(false);
//         set_grade_randomforest(
//           response.data.predicted_grade_from_random_forest_model
//         );
//         set_grade_decisiontree(
//           response.data.predicted_grade_from_decision_tree_model
//         );
//       })
//       .catch((error) => {
//         console.error(error);
//         alert("Invalid Credentials");
//         setLoading(false);
//       })
//       .finally(() => {
//         setLoading(false); // Set loading back to false when the request is complete
//       });
//   };

//   const generatePlot = () => {
//     // Make a GET request to the Flask endpoint that generates the plot
//     axios
//       .get("http://localhost:5000/generate_plot")
//       .then((response) => {
//         // Assuming the response contains the URL to the generated plot image
//         setPlotUrl(response.data); // Update state with the URL of the plot image
//       })
//       .catch((error) => {
//         console.error("Error fetching plot:", error);
//       });
//   };

//   return (
//     <>
//       <h1 className="heading">Welcome To Grade Prediction System</h1>
//       <div className="container">
//         <div className="text">
//           <h1 className="heading">View your predicted grade</h1>
//           <p className="paragraph">
//             View your predicted grade simply entering your symbol no. and name.
//           </p>

//           <form onSubmit={handleSubmit}>
//             <div>
//               <label className="label">Enter Symbol no:</label>
//               <input
//                 type="text"
//                 className="input"
//                 value={input1}
//                 placeholder="234039320"
//                 onChange={handleInputChange1}
//               />
//             </div>
//             <div>
//               <label className="label">Enter Name:</label>
//               <input
//                 type="text"
//                 className="input"
//                 placeholder="Simon Tamang"
//                 value={input2}
//                 onChange={handleInputChange2}
//               />
//             </div>
//             <button type="submit" className="button">
//               {loading ? (
//                 <p>loader</p>
//               ) : (
//                 // <Loader /> // Display the Loader component while loading
//                 "View" // Display "Login" text when not loading
//               )}
//             </button>

//             {grade_decisiontree && <h1>Decision Tree: {grade_decisiontree}</h1>}
//             {grade_randomforest && <h1>Random Forest: {grade_randomforest}</h1>}
//           </form>
//         </div>
//       </div>

//       <button onClick={generatePlot}>Generate Plot</button>

//       {plotUrl && (
//         <div>
//           <h3>Generated Plot:</h3>
//           <img src={plotUrl} alt="Generated Plot" />
//         </div>
//       )}
//     </>
//   );
// };

// export default HomeLayout;

import React from "react";

const HomeLayout = () => {
  return <div>HOmeLayout</div>;
};

export default HomeLayout;
