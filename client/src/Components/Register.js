import React, {useState} from 'react'
import { Container, Row, Col, Form, Button, Alert } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

function Register() {


    const navigate = useNavigate()
    const [authError, setAuthError] = useState(false)
    const [formData, setFormData] = useState({
      username:'',
      email:'',
      password:''
    })

    function handleChangeCaptureForm(event){
        setFormData({...formData, [event.target.name]: event.target.value})
      }

      function handleSubmitRegister(event){
        event.preventDefault()
        axios.post("/users", formData).then(res => {
          setAuthError(false)
          navigate("/login")
        }).catch(err => {
          setAuthError(err.response.data.detail.map((e) => e.msg))
        })
      }

  return (
    <Container style={{width: '50%'}}>
        <Row className='text-center my-5'>
            <h2>Register</h2>
        </Row>
        <Row className='px-4 my-5'>
        <Col >
            <Form onSubmit={(e)=>handleSubmitRegister(e)}>
                <Form.Group className="mb-3" controlId="email">
                    <Form.Label>Email</Form.Label>
                    <Form.Control name = "email" type="email" placeholder="Enter Email" onChange={handleChangeCaptureForm}/>
                </Form.Group>
                <Form.Group className="mb-3" controlId="username">
                    <Form.Label>Username</Form.Label>
                    <Form.Control name = "username" type="username" placeholder="Enter Username" onChange={handleChangeCaptureForm}/>
                </Form.Group>
                <Form.Group className="mb-3" controlId="formBasicPassword">
                    <Form.Label>Password</Form.Label>
                    <Form.Control name= "password" type="password" placeholder="Password" onChange={handleChangeCaptureForm}/>
                </Form.Group>
                <Button variant="success" type="submit">
                    Sign Up
                </Button>
            </Form>
        </Col>
        </Row>

        {authError ? <Alert className="text-center" variant='danger'>{authError}</Alert> : null}

    </Container>
  )
}

export default Register