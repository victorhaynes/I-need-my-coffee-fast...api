import './App.css';
import axios from "axios";
import { useState, useEffect } from 'react';


function App() {

  const [coffees, setCoffees] = useState([])

  useEffect(()=>{
    axios.get('/test').then(res => setCoffees(res.data));
  },[])

  return <>{coffees}</>

  // return (
  //   <>
  //     {coffees.map((c) => {
  //       return <>Test</>
  //     })}
  //   </>
  // );
}

export default App;
