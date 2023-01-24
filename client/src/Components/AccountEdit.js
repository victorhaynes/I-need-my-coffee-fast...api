import axios from 'axios'
import React, {useState, useEffect} from 'react'
import { Container, Row, Col, Form, Button, Alert } from 'react-bootstrap'

function AccountEdit({currentUser, setCurrentUser}) {


    const [submissionErrors, setSubmissionError] = useState(false)
    const [success, setSuccess] = useState(false)
    const [formData, setFormData] = useState({
        username:"",
        email:"",
        password: "",
    })

    function handleChangeCaptureForm(event){
        setFormData({...formData, [event.target.name]: event.target.value})
      }

    function handleSubmitEditAccount(event){
        event.preventDefault()
        axios.put(`/users/${currentUser?.id}`, formData, {
            headers: {
                'X-CSRF-TOKEN': currentUser?.csrf
            }
        }).then(res => {
            setFormData({
                username:"",
                email:"",
                password: "",
            })
            setSuccess(true)
            event.target.reset()
            setCurrentUser(res.data)
        }).catch(err => {
            setSubmissionError(err.response.data.detail.map((e) => e.msg))
            setSuccess(false)
        })
    }

  return (
    <Container style={{width: '50%'}}>
        <Row className='text-center my-5'>
            <h2>Edit Your Account</h2>
        </Row>
        <Row className='px-4 my-5'>
        <Col >
            <Form onSubmit={(e)=>handleSubmitEditAccount(e)}>
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
                    Update Account
                </Button>
            </Form>
        </Col>
        </Row>

        {success ? <Alert className="text-center" variant='info'>Edit successful.</Alert> :null}
        {submissionErrors ? <Alert className="text-center" variant='danger'>{submissionErrors}</Alert> : null}

    </Container>
  )
}

export default AccountEdit