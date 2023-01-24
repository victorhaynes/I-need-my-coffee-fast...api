import React from 'react'
import { Container, Row, Col, Image, Button } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'

function Account({currentUser, prettyDate}) {

  const navigate = useNavigate()

  function handleClick(){
    navigate(`/account/edit`)
  }

  return (
    <Container style={{width: "50%", backgroundColor: "whitesmoke", borderRadius: "10px", minWidth: "500px", outline: "5px solid grey"}} className='my-5'>
      <Row>
        <Col>
          <Image src="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460__340.png" 
                roundedCircle 
                alt="avatar" 
                fluid
                className='my-3 mx-auto'></Image>
        </Col>
        <Col>
        <h3 style={{marginTop: "10%"}}>Account Details</h3>
        <Container>
          <Row>
            <Col>
              <h5>Username:</h5>
              <p>{currentUser?.username}</p>
            </Col>
          </Row>
          <Row>
            <Col>
              <h5>Email:</h5>
              <p>{currentUser?.email}</p>
            </Col>
          </Row>
          <Row>
            <Col>
              <p className="text-muted">Signed up {prettyDate(currentUser?.time_created)}</p>
            </Col>
          </Row>
        </Container>
        </Col>
      </Row>
      <>
          {currentUser? <Button className="my-3 mx-3" variant="warning" onClick={handleClick}>Edit</Button> : null}
      </>
    </Container>
  )
}

export default Account

// https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460__340.png