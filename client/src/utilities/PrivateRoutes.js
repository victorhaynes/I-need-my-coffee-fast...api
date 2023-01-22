import React from 'react'
import { Navigate, Outlet } from 'react-router-dom'

function PrivateRoutes({currentUser}) {
    return (
        currentUser ? <Outlet/> : <Navigate to="/login"/>
    )
}

export default PrivateRoutes