import React from 'react'
import { Col, Container, Row, Image, Button, Card, Alert } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'


function Home({coffees, coffeesErrors}) {

  const navigate = useNavigate()

  function handleClick(){
    navigate("/coffees")
  }

  return (
    <>
      <Container>
        <Row className='px-4 my-5' >
            <Col sm={7}>
              <Image 
                src="https://www.tastingtable.com/img/gallery/what-is-terroir-and-does-it-matter-for-coffee-beans/l-intro-1645978396.jpg" 
                rounded
                alt="cofee beans" 
                fluid
                />
            </Col>
            <Col sm={5}>
              <h1>Welcome</h1>
              <p>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
              </p>
              <Button onClick={handleClick} variant="outline-dark">Explore Speciality Grade Coffee</Button>
            </Col>
        </Row>
        <Row>
          <Card className="text-center bg-secondary text-white my-5 py-4" >
            <Card.Body>Shop coffees from over 100 speciality roasters across North America and 25 unique, expressive origins. Each batch is roasted to order according to the roaster's schedule and subsequently shipped within 48 hours.</Card.Body>
          </Card>
        </Row>
        <Row className='text-center my-5'>
          <h1>Our Latest Offerings:</h1>
        </Row>
      </Container>
      <Container fluid style={{width: "70%"}}>
          <Row>
            <Col>    
              <Card style={{ width: '18rem' }} className="mx-auto">
                <Card.Img variant="top" src={coffees?.at(-1)?.image_url} />
                <Card.Body>
                  <Card.Title>{coffees?.at(-1)?.name}</Card.Title>
                  <Card.Text>
                    Producer: {coffees?.at(-1)?.roaster?.name}
                  </Card.Text>
                  <Button variant="success">See More</Button>
                </Card.Body>
              </Card>  
            </Col>
            <Col>    
              <Card style={{ width: '18rem' }} className="mx-auto">
                <Card.Img variant="top" src={coffees?.at(-2)?.image_url} />
                <Card.Body>
                <Card.Title>{coffees?.at(-2)?.name}</Card.Title>
                  <Card.Text>
                    Producer: {coffees?.at(-2)?.roaster?.name}
                  </Card.Text>
                  <Button variant="success">See More</Button>
                </Card.Body>
              </Card>  
            </Col>
          </Row> 
          {coffeesErrors ? <Alert variant='danger'>{coffeesErrors}</Alert> : null}
      </Container>
    </>
  )
}

export default Home