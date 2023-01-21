import axios from 'axios';
import React from 'react'
import {Navbar, Container, Nav, Button} from 'react-bootstrap'
import { Link } from 'react-router-dom';


function NavBar({currentUser, setCurrentUser}) {

    function logMeOut(){
        axios.delete("/logout").then(res => setCurrentUser(false))
    }

  return (
        <Navbar bg="dark" variant="dark">
            <Container>
                <Navbar.Brand as={Link} to="/">I Need My Coffee Fast(...API)</Navbar.Brand>
                <Nav className="me-auto">
                    <Nav.Link as={Link} to="/">Home</Nav.Link>
                    <Nav.Link as={Link} to="/coffees">Coffees</Nav.Link>
                    <Nav.Link as={Link} to="/roasters">Roasters</Nav.Link>
                    {currentUser ? <Button variant="success" onClick={logMeOut}>Logout</Button> : <Nav.Link as={Link} to="/login">Login</Nav.Link>}                  
                    <Nav.Link as={Link} to="/account">Account</Nav.Link>
                    <Nav.Link as={Link} to="/about">About</Nav.Link>
                </Nav>
            </Container>
        </Navbar>
  )
}

export default NavBar