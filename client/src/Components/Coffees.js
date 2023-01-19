import React from 'react'
import axios from "axios";
import { useState, useEffect } from 'react';
import { Card, Button, CardGroup, Row, Col } from 'react-bootstrap';


function Coffees({prettyDate}) {

    const [coffees, setCoffees] = useState([])
    const [errors, setErrors] = useState({})


    useEffect(()=>{
    axios.get('/coffees').then(res => setCoffees(res.data)).catch(err => setErrors(err));
    },[])


    return (
        <Row xs={1} md={2} className="g-4">
            {coffees?.map((coffee) => (
            <Col key={coffee.id}>
                <Card style={{ width: '18rem' }}>
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
  )
}

export default Coffees