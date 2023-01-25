import React, { useState } from "react"
import axios from "axios"
import { Container, Row, Col, Form, Button, Alert } from "react-bootstrap"

function RoastersNew({currentUser, setRoasters}) {



    const [error, setError] = useState(false)    
    const [success, setSuccess] = useState(false)

    const [formData, setFormData] = useState({
        name:""

    })


    function handleChangeCaptureForm(event){
        setFormData({...formData, [event.target.name]: event.target.value})
    }

    function handleSubmitPostRoaster(event){
        event.preventDefault()
        axios.post('/roasters', formData
        , 
        {
            headers: {
                'X-CSRF-TOKEN': currentUser?.csrf
            }
        }
        ).then(res => {
            setFormData({
            name:""
            })
            event.target.reset()
            setError(true)
            setSuccess(true)
            setRoasters((roasters) => [...roasters, res.data])
        })
        .catch(err => {
            setError(err.response.data.detail.map((e) => e.msg))
            setSuccess(false)
        })

      }

  return (
    <>
        <Container style={{width: '50%'}}>
            <Row className='text-center my-5'>
                <h2>Post New Roaster</h2>
            </Row>
            <Row className='px-4 my-5'>
            <Col >
                <Form onSubmit={(e)=>handleSubmitPostRoaster(e)}>
                    <Form.Group className="mb-3" controlId="name">
                        <Form.Label>Roaster Name:</Form.Label>
                        <Form.Control name="name" placeholder="Enter Coffee Name" onChange={handleChangeCaptureForm}/>
                    </Form.Group>
                    <Button variant="success" type="submit">
                        Submit
                    </Button>
                </Form>
            </Col>
            </Row>
        </Container> 


        {success ? <Alert className="text-center" variant='info'>Post successful.</Alert> : null}
        {error && !success ? <Alert className="text-center" variant='danger'>{error}</Alert> : null}
    </> 
  )
}

export default RoastersNew