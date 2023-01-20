import React from 'react'
import { Navigate, Outlet } from 'react-router-dom'

function PrivateRoutes({authenticatedUser}) {
    return (
        authenticatedUser?.access_token ? <Outlet/> : <Navigate to="/login"/>
    )
}

export default PrivateRoutes