import axios from 'axios'
import React, { useState, useEffect } from 'react'
import { Navigate, Outlet } from 'react-router-dom'

function PrivateRoutes({currentUser}) {

    const [loading, setLoading] = useState(true)

    useEffect(() => {
        axios.get("/me").then(res => {
        setLoading(false)
      })},[])

    return (
        <>
            {loading ? <></> : (currentUser ? <Outlet/> : <Navigate to="/login"/>)}
        </>
    )
}

export default PrivateRoutes