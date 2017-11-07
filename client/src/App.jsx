import React, { Component } from 'react';
import { Route, Switch } from 'react-router-dom'
import axios from 'axios';

import CulturesList from './components/CulturesList';
import AddCulture from './components/AddCulture';
import LinesList from './components/LinesList';
import NavBar from './components/NavBar';
import HomeWelcome from './components/HomeWelcome';
import Form from './components/Form';

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
      }
    }
  }
  componentDidMount() {
    this.getCultures();
  }
  getCultures() {
    axios.get('/api/cultures')
    .then((res) => { this.setState({ cultures: res.data.data.cultures }); })
    .catch((err) => { console.log(err); })
  }
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
  handleChange(event) {
    const obj = {};
    obj[event.target.name] = event.target.value;
    this.setState(obj);
  }
  render() {
    return (
      <div>
        <NavBar
          title={this.state.title}
        />
        <div className="container">
          <div className="row">
            <div className="col-md-3">
              <br/>
              <Switch>
                <Route exact path='/' component={HomeWelcome}/>
                <Route exact path='/library' render={() => ( 
                  <div>
                    <h1>All Cultures</h1>
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
                    <CulturesList cultures={this.state.cultures}/>
                  </div>
                )} />
                <Route exact path='/lines' component={LinesList}/>
                <Route exact path='/register' render={() => (
                  <Form
                    formType={'Register'}
                    formData={this.state.formData}
                  />
                )} />
                <Route exact path='/login' render={() => (
                  <Form
                    formType={'Login'}
                    formData={this.state.formData}
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
