import React from 'react'
import { Container, Row, Alert } from 'react-bootstrap'
import { useEffect, useState } from 'react'
import axios from 'axios'
import { Card, Col, Button } from 'react-bootstrap'
import { useParams, useNavigate } from 'react-router-dom'

function RoastersShow({prettyDate, currentUser, setRoasters, setCoffees, coffees}) {

    const params = useParams()
    const navigate = useNavigate()
    const [roaster, setRoaster] = useState(false)
    const [error, setError] = useState(false)

    useEffect(() => {
        axios.get(`/roasters/${params.id}`).then(res =>{ 
          setRoaster(res.data)
          setError(false)
        }).catch(err => setError(err.response.data.detail.map((e) => e.msg)))
      }, [])

      function handleClick(id){
        navigate(`/roasters/${id}`)
      }

      function handleDelete(){
        axios.delete(`/roasters/${roaster?.id}`,  {
          headers: {
            'X-CSRF-TOKEN': currentUser?.csrf
        }
        }).then(res => {
          setRoasters( (oldArray) => oldArray.filter((existingRoaster) => existingRoaster.id !== roaster?.id))
          setError(false)
          // Coffee state update - DELETE
          const coffeesNotOwnedByDeleted = [...coffees].filter((existingCoffee) => existingCoffee.roaster_id !== roaster.id)
          setCoffees(coffeesNotOwnedByDeleted)
          navigate("/roasters")
        })
        .catch(err => setError(err.response.data.detail.map((e) => e.msg)))
      }

  return (
    <Container style={{width: "40%"}}>
      { !error ? 
        <>
        <Row>
        <Col key={roaster.id} style={{marginBottom: "50px"}}>
            <Card style={{ width: '18rem' }} className="mx-auto my-5">
            <Card.Img variant="top" src={roaster.image_url} />
            <Card.Body>
                <Card.Title style={{fontSize: "190%"}}>{roaster.name}</Card.Title>
                <Card.Text>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
                </Card.Text>
            </Card.Body>
            <Card.Footer>
                    <small className="text-muted">Listed {prettyDate(roaster.time_created)}</small>
            </Card.Footer>
            { currentUser ? <Button className="my-30" variant="warning" onClick={ () => handleClick(roaster?.id)}>Edit</Button> : null}
            { currentUser?.username == "admin" ? <Button className="my-30" variant="danger" onClick={handleDelete}>Delete</Button> : null}
            </Card>
        </Col>
        <Col className='my-5' style={{borderRadius: "10px", outline: "2px solid rgba(0, 0, 0, 0.175)"}}>
            <h1>{roaster?.name}'s Coffees</h1>
            <ul>
                {roaster?.coffees?.map((c) => <li>{c.name}</li>)}
            </ul>
        </Col>
        </Row>
        </>
        : <Alert className="text-center my-auto" variant='danger'>{error}</Alert>}
    </Container>
  )
}

export default RoastersShow