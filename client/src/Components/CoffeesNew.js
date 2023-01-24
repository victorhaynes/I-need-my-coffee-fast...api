import React, {useState, useEffect} from 'react'
import { Row, Form, Col, Container, Button, Alert } from 'react-bootstrap'
import axios from 'axios'

function CoffeesNew({setCoffees, currentUser, roasters, setRoasters}) {


    const [error, setError] = useState(false)    
    const [success, setSuccess] = useState(false)

    const [formData, setFormData] = useState({
        name:"",
        roast:"",
        roaster_id: null,
        image_url: ""

    })

    // const [roasters, setRoasters] = useState([])
    // const [roastersError, setRoastersError] = useState(false)

    // useEffect(() => {
    //     axios.get('/roasters').then(res => {
    //         setRoasters(res.data)
    //         }).catch(err => {
    //             setRoastersError(err.response.data.detail.map((e) => e.msg))
    //             setSuccess(false)
    //         })
    //     }, [])

    function handleChangeCaptureForm(event){
        setFormData({...formData, [event.target.name]: event.target.value})
        
      }

    function handleSubmitPostCoffee(event){
        event.preventDefault()
        axios.post('/coffees', formData
        , 
        {
            headers: {
                'X-CSRF-TOKEN': currentUser?.csrf
            }
        }
        ).then(res => {
            setFormData({
            name:'',
            roast:'',
            roaster_id: null,
            image_url: ""
            })
            event.target.reset()
            setError(true)
            setSuccess(true)
            setCoffees((coffees) => [...coffees, res.data])
            // Roasters state update - POST
            const roasterToUpdate = [...roasters].filter((individualRoaster) => individualRoaster.id == res.data.roaster_id)[0]
            roasterToUpdate.coffees.push(res.data)
            console.log(roasterToUpdate)
            const updatedRoasterArray = [...roasters].map((existingRoaster) => {
                if(parseInt(existingRoaster.id) === parseInt(roasterToUpdate.id)){
                    return roasterToUpdate
                } else {
                    return existingRoaster
                }
            } )
            setRoasters(updatedRoasterArray)
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
                <h2>Post New Coffee</h2>
            </Row>
            <Row className='px-4 my-5'>
            <Col >
                <Form onSubmit={(e)=>handleSubmitPostCoffee(e)}>
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


        {success ? <Alert className="text-center" variant='info'>Post successful.</Alert> : null}
        {error && !success ? <Alert className="text-center" variant='danger'>Issue</Alert> : null}
    </> 
    )
}

export default CoffeesNew