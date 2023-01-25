import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Container, Col, Row, Image, Alert, Card, Button } from 'react-bootstrap'

function CoffeesShow({currentUser, prettyDate, setCoffees, roasters, setRoasters}) {

  const params = useParams()
  const navigate = useNavigate()
  const [coffee, setCoffee] = useState(false)
  const [error, setError] = useState(false)


  useEffect(() => {
    axios.get(`/coffees/${params.id}`).then(res =>{ 
      setCoffee(res.data)
      setError(false)
    }).catch(err => setError(err.response.data.detail.map((e) => e.msg)))
  }, [])

  function handleClick(){
    navigate(`/coffees/${coffee?.id}/edit`)
  }

  function handleDelete(){
    axios.delete(`/coffees/${coffee?.id}`,  {
      headers: {
        'X-CSRF-TOKEN': currentUser?.csrf
    }
    }).then(res => {
      setCoffees( (coffees) => coffees.filter((existingCoffee) => existingCoffee.id !== coffee?.id))
      setError(false)
      // Roasters state update - DELETE
      const roasterToUpdate = [...roasters].filter((individualRoaster) => individualRoaster.id == coffee.roaster_id)[0]
      console.log(roasterToUpdate)
      roasterToUpdate.coffees = roasterToUpdate?.coffees.filter((existingCoffee) => existingCoffee.id !== coffee?.id)
      const updatedRoasterArray = [...roasters].map((existingRoaster) => {
          if(parseInt(existingRoaster?.id) === parseInt(roasterToUpdate?.id)){
              return roasterToUpdate
          } else {
              return existingRoaster
          }
      } )
      console.log(roasterToUpdate)
      console.log(updatedRoasterArray)
      setRoasters(updatedRoasterArray)
      navigate("/coffees")
    })
    .catch(err => setError(err.response.data.detail.map((e) => e.msg)))

  }

  return (
    <Container fluid style={{width: "80%", backgroundColor: "whitesmoke", minWidth: "500px"}} className='my-5 square border rounded'>
      { !error ? 
        <>
          <Row>
            <Col >
              <Row>
                <Image src={coffee?.image_url} fluid></Image>
              </Row>
            </Col>
            <Col>
              <Row>
              <Row>
                <h3 style={{marginTop: "10%"}}>Name:</h3>
                <h5 style={{color: "grey"}}>{coffee?.name}</h5>
              </Row>
              <Row>
                <h3>Roast:</h3>
                <h5 style={{color: "grey"}}>{coffee?.roast}</h5>
              </Row>
              <Row>
                <h3>Roaster:</h3>
                <h5 style={{color: "grey"}}>{coffee?.roaster?.name}</h5>
              </Row>
                <h2>ABOUT THIS COFFEE:</h2>
                <p style={{color: "grey", marginBottom: "35px"}}>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
                </p>
              </Row>
            </Col>
          </Row>
          <Card.Footer>
            <p style={{marginLeft: "30%"}} className="text-muted">Listed {prettyDate(coffee.time_created)}</p>
          </Card.Footer>
        </>
       : <Alert className="text-center my-auto" variant='danger'>{error}</Alert>}
        <>
          {currentUser? <Button className="my-3 mx-3" variant="warning" onClick={handleClick}>Edit</Button> : null}
          {currentUser?.username == "admin" ? <Button className="my-3 mx-3" variant="danger" onClick={handleDelete}>Delete</Button> : null }
        </>

       
    </Container>
) 

}

export default CoffeesShow