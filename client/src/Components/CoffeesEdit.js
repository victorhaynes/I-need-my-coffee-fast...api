import React, {useState} from 'react'
import { Container, Col, Form, Row, Button, Select } from 'react-bootstrap'

function CoffeesEdit() {

    const [formData, setFormData] = useState({
        username:'',
        password:''
    })

    function handleChangeCaptureForm(event){
        setFormData({...formData, [event.target.name]: event.target.value})
      }

    function handleSubmitEditCoffee(event){
        event.preventDefault()
    }
  return (
    <Container style={{width: '50%'}}>
    <Row className='px-4 my-5'>
      <Col >
        <Form onSubmit={(e)=>handleSubmitEditCoffee(e)}>
          <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label>Name</Form.Label>
            <Form.Control name="name" placeholder="Enter Coffee Name" onChange={handleChangeCaptureForm}/>
          </Form.Group>
          <Form.Group className="mb-3" controlId="formBasicPassword">
            <Form.Label>Select Roast Level</Form.Label>
            <Form.Control as="select">
                <option value="Light">Light</option>
                <option value="Medium">Medium</option>
                <option value="Dark">Dark</option>
            </Form.Control>
          </Form.Group>
          <Button variant="success" type="submit">
            Submit
          </Button>
        </Form>
      </Col>
    </Row>
  </Container>  )
}

export default CoffeesEdit