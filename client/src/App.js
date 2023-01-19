import './App.css';
import axios from "axios";
import { useState, useEffect } from 'react';
import NavBar from './Components/NavBar';
import {BrowserRouter, createBrowserRouter,RouterProvider} from "react-router-dom";

function App() {

  const [coffees, setCoffees] = useState([])
  useEffect(()=>{
    axios.get('/test').then(res => setCoffees(res.data));
  },[])

  return (
    <BrowserRouter>
      <NavBar/>
      {coffees}
    </BrowserRouter>
  )

  // return (
  //   <>
  //     {coffees.map((c) => {
  //       return <>Test</>
  //     })}
  //   </>
  // );
}

export default App;
