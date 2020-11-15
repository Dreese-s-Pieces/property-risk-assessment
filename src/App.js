import React from 'react';
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
      result: {
        top_regional_offenses: [['', '', ''], ['', '', ''], ['', '', '']]
      },
    };
  }

  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  } 

  handleSubmit(event) {
    let url = '/data?state=' + this.state.state + '&zip=' + this.state.zip_code

    fetch(url).then(res => res.json()).then(data => {
      console.log(data);
      this.setState({result: data})

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
            <form onSubmit={this.handleSubmit}>

            <input className="address-input"
              name={"street_address"}
              value={this.state.street_address}
              placeholder={"Enter street address"}
              onChange={this.handleChange}
            />
            <br/>
            <input className="address-input"
              name={"city"}
              value={this.state.city}
              placeholder={"Enter city"}
              onChange={this.handleChange}
            />
            <br/>

            <input className="address-input"
              name={"state"}
              value={this.state.state}
              placeholder={"Enter state (Abbreviation)"}
              onChange={this.handleChange}
            />
            <br/>

            <input className="address-input"
              name={"zip_code"}
              value={this.state.zip_code}
              placeholder={"Enter zip code"}
              onChange={this.handleChange}
            />
            <br/>
            <input className="address-input"
              type="submit" 
              value="Submit"
            />
            </form>
          </div>

          <div className='display-container'>
            <h3>Input Address</h3>
            <div>
              <p>Street Address: {this.state.street_address}</p>
              <p>City: {this.state.city}</p>
              <p>State: {this.state.state}</p>
              <p>Zip Code: {this.state.zip_code}</p>
            </div>
            <br/>
            <h3>Weather Damage</h3>
            <div>
              <p>Total Damage for Zip: {this.state.result.total_dmg_for_zip}</p>
              <p>Total Damage for State: {this.state.result.total_dmg_for_state}</p>
              <p>Total Damage: {this.state.result.total_dmg}</p>
              <p>Property Damage for State: {this.state.result.prop_zip_dmg_for_state}</p>
              <p>Property Damage for Nation: {this.state.result.prop_zip_dmg_for_nation}</p>
            </div>
            <div>
              <h3>Top 3 Regional Offenses</h3>
              <ol>
                <li>{this.state.result.top_regional_offenses[0][0]}</li>
                <li>{this.state.result.top_regional_offenses[1][0]}</li>
                <li>{this.state.result.top_regional_offenses[2][0]}</li>
              </ol>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
