import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Form, Button, Container, Row, Col, } from 'react-bootstrap'

function Login({setCurrentUser, setAuthError}) {

  // const [errors, setErrors] = useState([])
  const [formData, setFormData] = useState({
    username:'',
    password:''
  })


  function handleChangeCaptureForm(event){
    setFormData({...formData, [event.target.name]: event.target.value})
  }

  function handleSubmitLogin(event){
    event.preventDefault()
    axios.post("/login", formData).then(res => {
      setCurrentUser(res.data)
      setAuthError(false)
    }).catch(err => {
      setAuthError(err.message)
      setCurrentUser(false)
    })
  }

  return (
    <Container style={{width: '50%'}}>
      <Row className='px-4 my-5'>
        <Col >
        <Form onSubmit={(e)=>handleSubmitLogin(e)}>
      <Form.Group className="mb-3" controlId="formBasicEmail">
        <Form.Label>Username</Form.Label>
        <Form.Control name = "username" type="username" placeholder="Enter Username" onChange={handleChangeCaptureForm}/>
        {/* <Form.Text className="text-muted">
          We'll never share your email with anyone else.
        </Form.Text> */}
      </Form.Group>

      <Form.Group className="mb-3" controlId="formBasicPassword">
        <Form.Label>Password</Form.Label>
        <Form.Control name= "password" type="password" placeholder="Password" onChange={handleChangeCaptureForm}/>
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