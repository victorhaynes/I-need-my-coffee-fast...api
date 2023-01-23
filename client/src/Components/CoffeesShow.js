import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Container, Col, Row, Image, Alert, Card } from 'react-bootstrap'

function CoffeesShow({prettyDate}) {

  const params = useParams()
  const [coffee, setCoffee] = useState(false)
  const [error, setError] = useState(false)


  useEffect(() => {
    axios.get(`/coffees/${params.id}`).then(res => setCoffee(res.data)).catch(err => setError(err.response.data.detail.map((e) => e.msg)))
  }, [])

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
    </Container>
) 

}

export default CoffeesShow