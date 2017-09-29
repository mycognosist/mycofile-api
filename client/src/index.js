import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import CulturesList from './components/CulturesList';

class App extends Component {
  constructor() {
    super()
    this.state = {
      cultures: []
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
  render() {
    return (
      <div className="container">
        <div className="row">
          <div className="col-md-4">
            <br/>
            <h1>All Cultures</h1>
            <hr/><br/>
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
