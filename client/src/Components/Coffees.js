import React from 'react'
import axios from "axios";
import { useState, useEffect } from 'react';
import { Card, Button, Container, Row, Col } from 'react-bootstrap';


function Coffees({prettyDate}) {

    const [coffees, setCoffees] = useState([])
    const [errors, setErrors] = useState({})


    useEffect(()=>{
    axios.get('/coffees').then(res => setCoffees(res.data)).catch(err => setErrors(err));
    },[])


    return (
        <Container fluid style={{width: "70%"}}>
            <Row>
                <div className='title-holder text-center my-4'>
                    <h2>Shop Speciality Coffees</h2>
                </div>
            </Row>
            <Row>
                {coffees?.map((coffee) => (
            <Col key={coffee.id} style={{marginBottom: "50px"}}>
                <Card style={{ width: '18rem' }} className="mx-auto">
                <Card.Img variant="top" src={coffee.image_url} />
                <Card.Body>
                    <Card.Title>{coffee.name}</Card.Title>
                    <Card.Text>Producer: {coffee.roaster.name}</Card.Text>
                </Card.Body>
                <Card.Footer>
                    <small className="text-muted">Listed {prettyDate(coffee.time_created)}</small>
                </Card.Footer>
                <Button className="my-30" variant="primary">See More</Button>
                </Card>
            </Col>
            ))}
            </Row>
        </Container>

  )
}

export default Coffees