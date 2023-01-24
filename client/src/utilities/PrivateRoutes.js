import axios from 'axios'
import React, { useState, useEffect } from 'react'
import { Navigate, Outlet, useNavigate } from 'react-router-dom'

function PrivateRoutes({currentUser, setCurrentUser}) {

    const [loading, setLoading] = useState(true)
    const [errors, setErrors] = useState(false)
    const navigate = useNavigate()

    useEffect(() => {
        axios.get("/me").then(res => {
        setLoading(false)
        setErrors(false)
        // this state update is necessary bc it grabs the CSRF token that "/login" cannot both generate & respond with at the same time
        setCurrentUser(res.data)
      }).catch((err) => setErrors(err.response?.data.detail.map((e) => e.msg)))}
      ,[])


    return (
        <>
            {errors ? <>{navigate("/login")}</> : <></>}
            {loading ? <></> : (currentUser ? <Outlet/> : <Navigate to="/login"/>)}
        </>
    )
}

export default PrivateRoutes

