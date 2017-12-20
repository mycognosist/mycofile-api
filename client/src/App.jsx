import React, { Component } from 'react';
import { Route, Switch } from 'react-router-dom'
import axios from 'axios';

import CulturesList from './components/CulturesList';
import AddCulture from './components/AddCulture';
import LinesList from './components/LinesList';
import AddLineObject from './components/AddLineObject';
import NavBar from './components/NavBar';
import HomeWelcome from './components/HomeWelcome';
import Form from './components/Form';
import Logout from './components/Logout';
import UserStatus from './components/UserStatus';

class App extends Component {
  constructor() {
    super()
    this.state = {
      cultures: [],
      genus: '',
      species: '',
      strain: '',
      unique_id: '',
      title: 'Mycofile',
      formData: {
        username: '',
        email: '',
        password: ''
      },
      isAuthenticated: false,
      lines: [],
      culture_id: '',
      container: '',
      dimensions: '',
      substrate: '',
      treatment: '',
      duration: '',
      path: '',
      id: '',
      user_id: ''
    }
  }
  componentDidMount() {
//    this.getCultures();
    this.getLines();
  }
  getLines() {
    axios.get('/api/lines')
    .then((res) => { this.setState({ lines: res.data.data.lines }); })
    .catch((err) => { console.log(err); })
  }
  addLineObject(event) {
    event.preventDefault();
    const data = {
      user_id: this.state.user_id,
      culture_id: this.state.culture_id,
      container: this.state.container,
      dimensions: this.state.dimensions,
      substrate: this.state.substrate,
      treatment: this.state.treatment,
      duration: this.state.duration
    }
    axios.post('/api/lines', data)
    .then((res) => {
      this.getLines();
      this.setState({
        culture_id: 'Culture ID',
        container: 'Container',
        dimensions: 'Dimensions',
        substrate: 'Substrate',
        treatment: 'Treatment',
        duration: 'Duration'
      });
    })
    .catch((err) => { console.log(err); })
  }
//  getCultures() {
//    axios.get('/api/cultures')
//    .then((res) => { this.setState({ cultures: res.data.data.cultures }); })
//    .catch((err) => { console.log(err); })
//  }
  addCulture(event) {
    event.preventDefault();
    const data = {
      genus: this.state.genus,
      species: this.state.species,
      strain: this.state.strain,
      unique_id: this.state.unique_id
    }
    axios.post('/api/cultures', data)
    .then((res) => {
      this.getCultures();
      this.setState({
        genus: 'Genus',
        species: 'Species',
        strain: 'Strain',
        unique_id: 'Unique ID'
      });
    })
    .catch((err) => { console.log(err); })
  }
  logoutUser() {
    window.localStorage.clear();
    this.setState({ isAuthenticated: false });
  }
  handleChange(event) {
    const obj = {};
    obj[event.target.name] = event.target.value;
    this.setState(obj);
  }
  handleUserFormSubmit(event) {
    event.preventDefault();
    const formType = window.location.href.split('/').reverse()[0];
    let data;
    if (formType === 'login') {
      data = {
        email: this.state.formData.email,
        password: this.state.formData.password
      }
    }
    if (formType === 'register') {
      data = {
        username: this.state.formData.username,
        email: this.state.formData.email,
        password: this.state.formData.password
      }
    }
    const url = `/api/auth/${formType}`;
    axios.post(url, data)
    .then((res) => {
      this.setState({
        formData: {username: '', email: '', password: '' },
        username: '',
        email: '',
        isAuthenticated: true
      });
      window.localStorage.setItem('authToken', res.data.auth_token);
      this.getCultures();
      this.getLines();
    })
    .catch((err) => { console.log(err); })
  }
  handleFormChange(event) {
    const obj = this.state.formData;
    obj[event.target.name] = event.target.value;
    this.setState(obj);
  }
  render() {
    return (
      <div>
        <NavBar
          title={this.state.title}
          isAuthenticated={this.state.isAuthenticated}
        />
        <div className="container">
          <div className="row">
            <div className="col-md-6">
              <br/>
              <Switch>
                <Route exact path='/' component={HomeWelcome}/>
                <Route exact path='/library' render={() => ( 
                  <div>
                    <CulturesList
                      isAuthenticated={this.state.isAuthenticated}
                      cultures={this.state.cultures}
                    />
                    <br/>
                    <h1>Add Culture</h1>
                    <hr/><br/>
                    <AddCulture
                      genus={this.state.genus}
                      species={this.state.species}
                      strain={this.state.strain}
                      unique_id={this.state.unique_id}
                      handleChange={this.handleChange.bind(this)}
                      addCulture={this.addCulture.bind(this)}
                    />
                    <br/>
                  </div>
                )} />
                <Route exact path='/lines' render={() => (
                  <div>
                    <LinesList lines={this.state.lines}/>
                    <br/>
                    <h1>Add Line Object</h1>
                    <hr/><br/>
                    <AddLineObject
                      culture_id={this.state.culture_id}
                      container={this.state.container}
                      dimensions={this.state.dimensions}
                      substrate={this.state.substrate}
                      treatment={this.state.treatment}
                      duration={this.state.duration}
                      handleChange={this.handleChange.bind(this)}
                      addLineObject={this.addLineObject.bind(this)}
                    />
                    <br/>
                  </div>
                )} />
                <Route exact path='/register' render={() => (
                  <Form
                    formType={'Register'}
                    formData={this.state.formData}
                    handleFormChange={this.handleFormChange.bind(this)}
                    handleUserFormSubmit={this.handleUserFormSubmit.bind(this)}
                    isAuthenticated={this.state.isAuthenticated}
                  />
                )} />
                <Route exact path='/login' render={() => (
                  <Form
                    formType={'Login'}
                    formData={this.state.formData}
                    handleFormChange={this.handleFormChange.bind(this)}
                    handleUserFormSubmit={this.handleUserFormSubmit.bind(this)}
                    isAuthenticated={this.state.isAuthenticated}
                  />
                )} />
                <Route exact path='/logout' render={() => (
                  <Logout
                    logoutUser={this.logoutUser.bind(this)}
                    isAuthenticated={this.state.isAuthenticated}
                  />
                )} />
                <Route exact path='/status' render={() => (
                  <UserStatus
                    isAuthenticated={this.state.isAuthenticated}
                  />
                )} />
              </Switch>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default App
