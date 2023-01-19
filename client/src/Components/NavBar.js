import React from 'react'
import {Navbar, Container, Nav} from 'react-bootstrap'
import {Link, Route, Routes} from "react-router-dom";
import Coffees from './Coffees';
import Home from './Home';
import Roasters from './Roasters';
import Login from './Login';
import Account from './Account';
import About from './About';

function NavBar() {
  return (
    <>
        <Navbar bg="dark" variant="dark">
            <Container>
                <Navbar.Brand as={Link} to="/">I Need My Coffee Fast(API)</Navbar.Brand>
                <Nav className="me-auto">
                    <Nav.Link as={Link} to="/">Home</Nav.Link>
                    <Nav.Link as={Link} to="/coffees">Coffees</Nav.Link>
                    <Nav.Link as={Link} to="/roasters">Roasters</Nav.Link>
                    <Nav.Link as={Link} to="/login">Login</Nav.Link>
                    <Nav.Link as={Link} to="/account">Account</Nav.Link>
                    <Nav.Link as={Link} to="/about">About</Nav.Link>
                </Nav>
            </Container>
        </Navbar>
        <Routes>
            <Route path="/" element={<Home/>}/>
            <Route path="/coffees" element={<Coffees/>}/>
            <Route path="/roasters" element={<Roasters/>}/>
            <Route path="/login" element={<Login/>}/>
            <Route path="/account" element={<Account/>}/>
            <Route path="/about" element={<About/>}/>
        </Routes>
    </>
  )
}

export default NavBar