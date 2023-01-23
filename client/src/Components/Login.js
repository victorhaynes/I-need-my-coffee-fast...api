import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Form, Button, Container, Row, Col, Alert, } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'


function Login({setCurrentUser}) {

  const navigate = useNavigate()
  const [authError, setAuthError] = useState(false)
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
      navigate("/account")
    }).catch(err => {
      setAuthError(err.response.data.detail.map((e) => e.msg))
      setCurrentUser(false)
    })
  }

  return (
    <>
      <Container style={{width: '50%'}}>
        <Row className='text-center my-5'>
            <h2>Login</h2>
        </Row>
        <Row className='px-4 my-5'>
          <Col >
            <Form onSubmit={(e)=>handleSubmitLogin(e)}>
              <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Username</Form.Label>
                <Form.Control name = "username" type="username" placeholder="Enter Username" onChange={handleChangeCaptureForm}/>
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

    {authError ? <Alert className="text-center" variant='danger'>{authError}</Alert> : null}
   </>

  )
}

export default Login