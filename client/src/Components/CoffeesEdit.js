import React, {useState, useEffect} from 'react'
import { Container, Col, Form, Row, Button, Alert } from 'react-bootstrap'
import { useParams } from 'react-router-dom'
import axios from 'axios'

function CoffeesEdit({coffees, setCoffees, currentUser}) {

    const [coffee, setCoffee] = useState(false)
    const [coffeeError, setCoffeError] = useState(false)
    const [roasters, setRoasters] = useState([])
    const [roastersError, setRoastersError] = useState(false)
    const [success, setSuccess] = useState(false)

    const params = useParams()
 
    useEffect(() => {
      axios.get(`/coffees/${params.id}`).then(res => setCoffee(res.data)).catch(err => setCoffeError(err.response.data.detail.map((e) => e.msg)))
    }, [])

    useEffect(() => {
        axios.get('/roasters').then(res => setRoasters(res.data)).catch(err => setRoastersError(err.response.data.detail.map((e) => e.msg)))
      }, [])

      
    const [formData, setFormData] = useState({
        name:"",
        roast:"",
        roaster_id: null,
        image_url: ""

    })

    const [submissionErrors, setSubmissionError] = useState(false)

    function handleChangeCaptureForm(event){
        setFormData({...formData, [event.target.name]: event.target.value})
      }

    function handleSubmitEditCoffee(event){
        event.preventDefault()
        axios.put(`/coffees/${params.id}`, formData, {
            headers: {
                'X-CSRF-TOKEN': currentUser?.csrf
            }
        }).then(res => {
            setFormData({
                name:'',
                roast:'',
                roaster_id: null,
                image_url: ""
            })
            setSuccess(true)
            event.target.reset()
            setCoffees(coffees?.map((individualCoffee) => {
                if(parseInt(individualCoffee.id) === parseInt(res.data.id)){
                    return res.data
                } else {
                    return individualCoffee
                }
            }))
        }).catch(err => {
            setSubmissionError(err.response.data.detail.map((e) => e.msg))
            setSuccess(false)
        })

    }

  return (
    <>
        <Container style={{width: '50%'}}>
            <Row className='text-center my-5'>
                <h2>Edit {coffee?.roaster?.name}'s {coffee?.name}</h2>
            </Row>
            <Row className='px-4 my-5'>
            <Col >
                <Form onSubmit={(e)=>handleSubmitEditCoffee(e)}>
                    <Form.Group className="mb-3" controlId="name">
                        <Form.Label>Name</Form.Label>
                        <Form.Control name="name" placeholder="Enter Coffee Name" onChange={handleChangeCaptureForm}/>
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="roast">
                        <Form.Label>Select Roast Level</Form.Label>
                        <Form.Control as="select" name="roast" onChange={handleChangeCaptureForm}>
                            <option value="">Select an option.</option>
                            <option value="Light">Light</option>
                            <option value="Medium">Medium</option>
                            <option value="Dark">Dark</option>
                        </Form.Control>
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="Roaster">
                        <Form.Label>Select Roaster Name</Form.Label>
                        <Form.Control as="select" name ="roaster_id" onChange={handleChangeCaptureForm}>
                        {[{name: "Select an option.", id: null},...roasters]?.map((roaster) => <option value={roaster.id}>{roaster.name}</option>)}
                        </Form.Control>
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="image_url">
                        <Form.Label>Image URL:</Form.Label>
                        <Form.Control name="image_url" placeholder="Enter image url" onChange={handleChangeCaptureForm}/>
                    </Form.Group>
                    <Button variant="success" type="submit">
                        Submit
                    </Button>
                </Form>
            </Col>
            </Row>
        </Container> 

        {success ? <Alert className="text-center" variant='info'>Edit successful.</Alert> :null}

        {submissionErrors && !success ? <Alert className="text-center" variant='Warning'>{submissionErrors}</Alert> : null}
    </> 
    )
}

export default CoffeesEdit