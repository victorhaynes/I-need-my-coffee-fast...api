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
import NotFound404 from './Components/Notfound404';
import 'bootstrap/dist/css/bootstrap.min.css';
import Footer from './Components/Footer';
import PrivateRoutes from './utilities/PrivateRoutes';
import NiceTry401 from './Components/NiceTry401';
import CoffeesShow from './Components/CoffeesShow';
import CoffeesEdit from './Components/CoffeesEdit';

function App() {
  
  // Get current user (hit API & check if JWT stored in cookies/valid), respond with a User object/dict for current user
  const [currentUser, setCurrentUser] = useState(false)
  useEffect(()=>{
    axios.get('/me').then(res => setCurrentUser(res.data)).catch(err => setCurrentUser(false));
  },[])

  // Fetch array of coffee objects
  const [coffees, setCoffees] = useState([])
  const [coffeesErrors, setCoffeesErrors] = useState(false)
  useEffect(()=>{
    axios.get('/coffees').then(res => setCoffees(res.data)).catch(err => setCoffeesErrors(err.response.data.detail));
  },[])

  // Date formatting function
  function prettyDate(time){
    const milliseconds = Date.parse(time)
    const dateified = new Date(milliseconds).toString().split(" GMT")[0]
    return dateified
}


  return (
    <BrowserRouter>
      <NavBar currentUser={currentUser} setCurrentUser={setCurrentUser}/>
      <Routes>
        <Route exact path ="/" element={<Home coffees={coffees} coffeesErrors={coffeesErrors} prettyDate={prettyDate}/>}/>
        <Route exact path ="/coffees" element={<Coffees prettyDate={prettyDate}/>}/>
        <Route exact path ="/coffees/:id" element={<CoffeesShow prettyDate={prettyDate}/>}/>
        <Route element={<PrivateRoutes currentUser={currentUser}/>}>
          <Route exact path ="/coffees/:id/edit" element={<CoffeesEdit prettyDate={prettyDate}/>}/>
        </Route>
        <Route exact path ="/roasters" element={<Roasters prettyDate={prettyDate}/>}/>
        <Route exact path ="/login" element={<Login setCurrentUser={setCurrentUser}/>}/>
        <Route element={<PrivateRoutes currentUser={currentUser}/>}>
          <Route exact path ="/account" element={<Account currentUser={currentUser} prettyDate={prettyDate}/>}/>
        </Route>
        <Route exact path ="/nice-try" element={<NiceTry401/>}/>
        <Route path="*" element={<NotFound404/>}/>
      </Routes>
      <Footer/>
    </BrowserRouter>
  )
}

export default App;
