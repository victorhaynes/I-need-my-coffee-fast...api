import React from 'react'
import axios from 'axios'
import { useState, useEffect } from 'react'

function Roasters() {


    const [roasters, setRoasters] = useState([])
    const [errors, setErrors] = useState([])

    useEffect(()=>{
    axios.get('/test').then(res => setRoasters(res.data)).catch(err => setErrors(err));
    },[])

    return (
        <div>
          {errors?.name}
          {errors?.message}
          {errors?.response?.data?.detail}  
        </div>
    )
}

export default Roasters