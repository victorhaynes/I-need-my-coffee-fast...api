import React, { useState } from 'react'
import axios from 'axios'
import { Form, Button, Container, Row, Col, } from 'react-bootstrap'

function Login({setAuthenticatedUser}) {

  const [errors, setErrors] = useState([])
  const [formData, setFormData] = useState({
    username:'',
    password:''
  })
  
  // function logMeIn(event){
  //   event.preventDefault()
  //   axios.post("/login", {
  //     username: "admin",
  //     password: "admin"
  //   }).then(res => setAuthenticatedUser(res.data)).catch(err => setErrors(err.message))
  // }

  function handleChange(event){
    setFormData({...formData, [event.target.name]: event.target.value})
  }

  function handleSubmit(event){
    event.preventDefault()
    axios.post("/login", formData).then(res => setAuthenticatedUser(res.data)).catch(err => setErrors(err.message))
  }

  return (
    <Container style={{width: '50%'}}>
      <Row className='px-4 my-5'>
        <Col >
        <Form onSubmit={(e)=>handleSubmit(e)}>
      <Form.Group className="mb-3" controlId="formBasicEmail">
        <Form.Label>Username</Form.Label>
        <Form.Control name = "username" type="username" placeholder="Enter Username" onChange={handleChange}/>
        {/* <Form.Text className="text-muted">
          We'll never share your email with anyone else.
        </Form.Text> */}
      </Form.Group>

      <Form.Group className="mb-3" controlId="formBasicPassword">
        <Form.Label>Password</Form.Label>
        <Form.Control name= "password" type="password" placeholder="Password" onChange={handleChange}/>
      </Form.Group>
      <Button variant="success" type="submit">
        Submit
      </Button>
    </Form>
        </Col>
      </Row>
   </Container>

  )
}

export default Login