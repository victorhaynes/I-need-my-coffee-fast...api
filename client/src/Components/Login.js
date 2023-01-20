import React, { useState } from 'react'
import axios from 'axios'
import { Form, Button, Container, Row, Col } from 'react-bootstrap'

function Login({setAuthenticatedUser}) {

  const [errors, setErrors] = useState([])

  function logMeIn(event){
    event.preventDefault()
    axios.post("/login", {
      username: "admin",
      password: "admin"
    }).then(res => setAuthenticatedUser(res.data)).catch(err => setErrors(err.message))
  }

  return (
    <Container style={{width: '50%'}}>
      <Row className='px-4 my-5'>
        <Col >
        <Form>
      <Form.Group className="mb-3" controlId="formBasicEmail">
        <Form.Label>Email address</Form.Label>
        <Form.Control type="email" placeholder="Enter email" />
        <Form.Text className="text-muted">
          We'll never share your email with anyone else.
        </Form.Text>
      </Form.Group>

      <Form.Group className="mb-3" controlId="formBasicPassword">
        <Form.Label>Password</Form.Label>
        <Form.Control type="password" placeholder="Password" />
      </Form.Group>
      <Button onClick={(e)=>logMeIn(e)}variant="success" type="submit">
        Submit
      </Button>
    </Form>
        </Col>
      </Row>
   </Container>

  )
}

export default Login