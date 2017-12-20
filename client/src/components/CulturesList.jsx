import React, { Component } from 'react';
import { Table } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import axios from 'axios';

class CulturesList extends Component {
  constructor (props) {
    super(props)
    this.state = {
//      cultures: [],
      user_id: '',
//      id: '',
//      culture_id: '',
//      genus: '',
//      species: '',
//      strain: ''
    }
  }
  componentDidMount() {
    if (this.props.isAuthenticated) {
      this.getUserStatus();
      this.getCulturesList();
    }
  }
  getUserStatus(event) {
    const options = {
      url: '/api/auth/status',
      method: 'get',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${window.localStorage.authToken}`
      }
    };
    return axios(options)
    .then((res) => {
      this.setState({
        user_id: res.data.data.id
      })
    })
    .catch((error) => { console.log(error); })
  }
  getCulturesList(event) {
    console.log(this.state.user_id);
    const options = {
      url: '/api/1/cultures',
      method: 'get',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${window.localStorage.authToken}`
      }
    };
    return axios(options)
      .then((res) => { this.setState({ cultures: res.data.data.cultures }); })
//      this.setState({
//        id: res.data.data.id,
//        culture_id: res.data.data.culture_id,
//        genus: res.data.data.genus,
//        species: res.data.data.species,
//        strain: res.data.data.strain
//      })
//    })
    .catch((error) => { console.log(error); })
  }
  render() {
    if (!this.props.isAuthenticated) {
      return <p>You must be logged in to view this. Click <Link to="/login">here</Link> to log in.</p>
    }
    this.props.cultures.map((culture) => {
      return (
        <div>
          <h1>Culture Library</h1>
          <hr/><br/>
          <Table striped bordered condensed hover>
            <thead>
              <tr>
                <th>ID</th>
                <th>Culture ID</th>
                <th>Genus</th>
                <th>Species</th>
                <th>Strain</th>
              </tr>
            </thead>
            <tbody>
              <tr key={this.state.id}>
                <td>{this.state.id}</td>
                <td>{culture.culture_id}</td>
                <td>{culture.genus}</td>
                <td>{culture.species}</td>
                <td>{culture.strain}</td>
              </tr>
            </tbody>
          </Table>
        </div>
      )
    })
  }  
}

export default CulturesList;
