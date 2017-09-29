import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import CulturesList from './components/CulturesList';
import AddCulture from './components/AddCulture';

class App extends Component {
  constructor() {
    super()
    this.state = {
      cultures: [],
      genus: '',
      species: '',
      strain: '',
      unique_id: ''
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
      <div className="container">
        <div className="row">
          <div className="col-md-6">
            <br/>
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
        </div>
      </div>
    )
  }
}

ReactDOM.render(
  <App />,
  document.getElementById('root')
);
