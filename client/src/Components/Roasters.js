import React from 'react'
import axios from 'axios'
import { useState, useEffect } from 'react'
import { Container, Row, Col, Card, Button } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'

function Roasters() {

    const navigate = useNavigate()
    const [roasters, setRoasters] = useState([])
    const [errors, setErrors] = useState([])

    useEffect(()=>{
    axios.get('/roasters').then(res => setRoasters(res.data)).catch(err => setErrors(err));
    },[])

    function handleClick(id){
      navigate(`/roasters/${id}`)
    }

    return (
      <Container fluid style={{width: "70%"}}>
        <Row>
            <div className='title-holder text-center my-4'>
                <h2>Our Partnered Roasters:</h2>
            </div>
        </Row>
        <Row>
            {roasters?.map((roaster) => (
        <Col key={roaster.id} style={{marginBottom: "50px"}}>
            <Card style={{ width: '18rem' }} className="mx-auto">
            <Card.Img variant="top" src={roaster.image_url} />
            <Card.Body>
                <Card.Title>{roaster.name}</Card.Title>
            </Card.Body>
            <Button className="my-30" variant="success" onClick={ () => handleClick(roaster?.id)}>Learn More</Button>
            </Card>
        </Col>
        ))}
        </Row>
        <Row>
            <Button variant='outline-success' onClick={()=>navigate("/roasters/new")}>
                Post New roaster
            </Button>
        </Row>
      </Container>
    )
}

export default Roasters