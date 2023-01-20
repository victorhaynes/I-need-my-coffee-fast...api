import React from 'react'
import { Navigate, Outlet } from 'react-router-dom'

function AdminRoutes() {
    const auth = {"token": false}
    return (
        auth.token ? <Outlet/> : <Navigate to="/nice-try"/>
    )
}

export default AdminRoutes