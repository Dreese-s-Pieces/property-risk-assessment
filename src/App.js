import React, { useState, useEffect } from 'react';
import './App.css';

export default App;

function App() {
  return (
    <TopComponent/>
  );
}

class TopComponent extends React.Component {
  constructor(props) {
    super(props);

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);

    this.state = {
      street_address: '',
      city: '',
      state: '',
      zip_code: '',
      total_dmg_for_zip: '',
    };
  }

  handleChange(event) {
    console.log(event.target.name)
    this.setState({[event.target.name]: event.target.value});
  } 

  handleSubmit(event) {
    alert('Searching for address: ' + this.state.street_address);

    let url = '/disaster/state_level_disasters?state=' + this.state.state + '&zip=' + this.state.zip_code

    fetch(url).then(res => res.json()).then(data => {
      console.log(data);
    });

    event.preventDefault();
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          Property Risk Assessment
        </header>
        <div className='row-container'>
          <div className='address-form'>
            <AddressForm 
              state="state"
              onSubmit={this.handleSubmit}
              onChange={this.handleChange} />
          </div>

          <div className='display-container'>
            <Display
              state="state" />
          </div>
        </div>
      </div>
    );
  }
}

class AddressForm extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <form onSubmit={this.props.onSubmit}>

        <input className="address-input"
          name={"street_address"}
          value={this.props.state.street_address}
          placeholder={"Enter street address"}
          onChange={this.props.OnChange}
        />
        <br/>
        <input className="address-input"
          name={"city"}
          value={this.props.state.city}
          placeholder={"Enter city"}
          onChange={this.props.OnChange}
        />
        <br/>

        <input className="address-input"
          name={"state"}
          value={this.props.state.state}
          placeholder={"Enter state"}
          onChange={this.props.OnChange}
        />
        <br/>

        <input className="address-input"
          name={"zip_code"}
          value={this.props.state.zip_code}
          placeholder={"Enter zip code"}
          onChange={this.props.OnChange}
        />
        <br/>
        <input className="address-input"
          type="submit" 
          value="Submit"
        />
      </form>
    );
  }
}

class Display extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <p>Total Damage for Zip: {this.props.state.total_dmg_for_zip}</p>
    );
  }
}
