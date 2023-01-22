import React from 'react'
import { Container, Row, Col, Image } from 'react-bootstrap'

function Account({currentUser, prettyDate}) {



  return (
    <Container style={{width: "50%", backgroundColor: "silver", borderRadius: "10px"}} className='my-5'>
      <Row>
        <Col>
        {/* <Row> */}
          <Image src="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460__340.png" 
                roundedCircle 
                alt="avatar" 
                // style={{width: "80%", height: "auto"}}
                fluid
                className='my-3 mx-auto'></Image>
                {/* </Row> */}
        </Col>
        <Col>
        <h3 style={{marginTop: "5px"}}>Account Details</h3>
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
    </Container>
  )
}

export default Account

// https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460__340.png