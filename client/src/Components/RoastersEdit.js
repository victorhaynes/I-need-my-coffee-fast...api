import React, {useState, useEffect} from 'react'
import { Container, Col, Form, Row, Button, Alert } from 'react-bootstrap'
import { useParams } from 'react-router-dom'
import axios from 'axios'
function RoastersEdit({setCoffees, currentUser, coffees, setRoasters}) {
    
    const [roaster, setRoaster] = useState(false)
    const [roasterError, setRoasterError] = useState(false)
    const [success, setSuccess] = useState(false)
    const [submissionErrors, setSubmissionError] = useState(false)

    const params = useParams()
 
    useEffect(() => {
      axios.get(`/roasters/${params.id}`).then(res => setRoaster(res.data)).catch(err => setRoasterError(err.response.data.detail.map((e) => e.msg)))
    }, [])

    const [formData, setFormData] = useState({
        name:"",
        id: parseInt(params.id)
    })

    function handleChangeCaptureForm(event){
        setFormData({...formData, [event.target.name]: event.target.value})
    }

    function handleSubmitEditRoaster(event){
        event.preventDefault()
        axios.put(`/roasters/${params.id}`, formData, {
            headers: {
                'X-CSRF-TOKEN': currentUser?.csrf
            }
        }).then(res => {
            setFormData({
                name:'',
                id: parseInt(params.id)
            })
            setSuccess(true)
            setRoaster(res.data)
            event.target.reset()
            setRoasters((oldArray) => oldArray?.map((individualRoaster) => {
                if(parseInt(individualRoaster.id) === parseInt(res.data.id)){
                    return res.data
                } else {
                    return individualRoaster
                }
            }))
            // Coffees state update - UPDATE
            const copyOfCoffees = [...coffees]
            const updatedCoffees = copyOfCoffees.map((individualCoffee) => {
                if (individualCoffee.roaster.id == res.data.id){
                    return {...individualCoffee, "roaster": res.data}
                } else {
                    return individualCoffee
                }
            })
            setCoffees(updatedCoffees)

        })
        .catch(err => {
            setSubmissionError(err.response.data.detail.map((e) => e.msg))
            setSuccess(false)
        })

    }

  return (
    <>
        <Container style={{width: '50%'}}>
            <Row className='text-center my-5'>
                <h2>Edit Roaster: {roaster?.name}</h2>
            </Row>
            <Row className='px-4 my-5'>
            <Col >
                <Form onSubmit={(e)=>handleSubmitEditRoaster(e)}>
                    <Form.Group className="mb-3" controlId="name">
                        <Form.Label>Roaster Name:</Form.Label>
                        <Form.Control name="name" placeholder="Enter Roaster Name" onChange={handleChangeCaptureForm}/>
                    </Form.Group>
                    <Button variant="success" type="submit">
                        Submit
                    </Button>
                </Form>
            </Col>
            </Row>
        </Container> 


        {success ? <Alert className="text-center" variant='info'>Edit successful.</Alert> : null}
        {submissionErrors && !success ? <Alert className="text-center" variant='danger'>{roasterError}</Alert> : null}
    </> 
  )
}

export default RoastersEdit