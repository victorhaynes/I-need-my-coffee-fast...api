import './App.css';
import axios from "axios";
import { useState, useEffect } from 'react';
import NavBar from './Components/NavBar';
import {BrowserRouter, Routes, createBrowserRouter,RouterProvider, Route} from "react-router-dom";
import Coffees from './Components/Coffees';
import Home from './Components/Home';
import Roasters from './Components/Roasters';
import Account from './Components/Account';
import Login from './Components/Login';
import About from './Components/About';
import NotFound404 from './Components/Notfound404';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  
  const [coffees, setCoffees] = useState([])
  const [errors, setErrors] = useState({})


  useEffect(()=>{
  axios.get('/coffees').then(res => setCoffees(res.data)).catch(err => setErrors(err));
  },[])

  function prettyDate(time){
    const milliseconds = Date.parse(time)
    const dateified = new Date(milliseconds).toString().split(" GMT")[0]
    return dateified
}


  return (
    <BrowserRouter>
      <NavBar/>
      <Routes>
        <Route exact path ="/" element={<Home coffees={coffees} prettyDate={prettyDate}/>}/>
        <Route exact path ="/coffees" element={<Coffees prettyDate={prettyDate}/>}/>
        <Route exact path ="/roasters" element={<Roasters prettyDate={prettyDate}/>}/>
        <Route exact path ="/login" element={<Login/>}/>
        <Route exact path ="/account" element={<Account/>}/>
        <Route exact path ="/about" element={<About/>}/>
        <Route path="*" element={<NotFound404/>}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App;
