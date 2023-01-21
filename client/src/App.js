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
import Footer from './Components/Footer';
import PrivateRoutes from './utilities/PrivateRoutes';
import NiceTry401 from './Components/NiceTry401';

function App() {
  
  const [currentUser, setCurrentUser] = useState(false)
  const [authError, setAuthError] = useState(false)
  // Get current user (hit API & check if JWT stored in cookies/valid), respond with a User object/dict for current user
  useEffect(()=>{
    axios.get('/me').then(res => {
      setCurrentUser(res.data)
      setAuthError(false)
    }).catch(err => {
      // setAuthError(err.message)
      setCurrentUser(false)
    });
  },[])

  const [coffees, setCoffees] = useState([])
  const [errors, setErrors] = useState({})
  // Fetch array of coffee objects
  useEffect(()=>{
    axios.get('/coffees').then(res => setCoffees(res.data)).catch(err => setErrors(err.message));
  },[])

  console.log(`current user ${currentUser.username}`)
  console.log(`coffees ${coffees[0]?.name}`)



  function prettyDate(time){
    const milliseconds = Date.parse(time)
    const dateified = new Date(milliseconds).toString().split(" GMT")[0]
    return dateified
}


  return (
    <BrowserRouter>
      <NavBar currentUser={currentUser} setCurrentUser={setCurrentUser}/>
      <Routes>
        <Route exact path ="/" element={<Home coffees={coffees} prettyDate={prettyDate}/>}/>
        <Route exact path ="/coffees" element={<Coffees prettyDate={prettyDate}/>}/>
        <Route exact path ="/roasters" element={<Roasters prettyDate={prettyDate}/>}/>
        <Route exact path ="/login" element={<Login setCurrentUser={setCurrentUser} setAuthError={setAuthError}/>}/>
        <Route element={<PrivateRoutes currentUser={currentUser}/>}>
          <Route exact path ="/account" element={<Account/>}/>
        </Route>
        <Route exact path ="/about" element={<About/>}/>
        <Route exact path ="/nice-try" element={<NiceTry401/>}/>
        <Route path="*" element={<NotFound404/>}/>
      </Routes>
      <Footer/>
    </BrowserRouter>
  )
}

export default App;
