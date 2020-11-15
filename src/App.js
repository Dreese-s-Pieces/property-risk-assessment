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
        total_dmg_for_zip: 0,
        total_dmg_for_state: 0,
        total_dmg: 0,
        prop_zip_dmg_for_state: 0,
        prop_zip_dmg_for_nation: 0,
        top_regional_offenses: [['', '', ''], ['', '', ''], ['', '', '']],
        deviation: '',
        probability: ''
      },
    };
  }

  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  } 

  handleSubmit(event) {
    let url = '/data?state=' + this.state.state + '&zip=' + this.state.zip_code + '&city=' + this.state.city

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
              <table>
                <tr>
                  <td className="table-label">Street Address:</td>
                  <td>{this.state.street_address}</td>
                </tr>
                <tr>
                  <td className="table-label">City:</td>
                  <td>{this.state.city}</td>
                </tr>
                <tr>
                  <td className="table-label">State:</td>
                  <td>{this.state.state}</td>
                </tr>
                <tr>
                  <td className="table-label">Zip Code:</td>
                  <td>{this.state.zip_code}</td>
                </tr> 
              </table>
            </div>
            <hr/>
            <h3>Weather Damage</h3>
            <div>
              <table>
                <tr>
                  <td className="table-label">Total Damage for Zip Code:</td>
                  <td className="table-data">${this.state.result.total_dmg_for_zip.toFixed(2)}</td>
                </tr>
                <tr>
                  <td className="table-label">Total Damage for State:</td>
                  <td className="table-data">${this.state.result.total_dmg_for_state.toFixed(2)}</td>
                </tr>
                <tr>
                  <td className="table-label">Total Damage:</td>
                  <td className="table-data">${this.state.result.total_dmg.toFixed(2)}</td>
                </tr>
                <tr>
                  <td className="table-label">Property Damage for State:</td>
                  <td className="table-data">${this.state.result.prop_zip_dmg_for_state.toFixed(2)}</td>
                </tr>
                <tr>
                  <td className="table-label">Property Damage for Nation:</td>
                  <td className="table-data">${this.state.result.prop_zip_dmg_for_nation.toFixed(2)}</td>
                </tr>
              </table>
            </div>

            <hr/>
            <div>
              <h3>Top 3 Regional Offenses</h3>
              <ol>
                <li>{this.state.result.top_regional_offenses[0][0]}</li>
                <li>{this.state.result.top_regional_offenses[1][0]}</li>
                <li>{this.state.result.top_regional_offenses[2][0]}</li>
              </ol>
            </div>

            <hr/>

            <div>
              <h3>Air Quality</h3>
              <table>
                <tr>
                  <td className="table-label">Deviation of AQI From Closest Cities: </td>
                  <td className="table-data">{this.state.result.deviation}</td>
                </tr>
                <tr>
                  <td className="table-label">Probability of AQI Being Significantly Better From Surrounding Cities: </td>
                  <td className="table-data">{this.state.result.probability}</td>
                </tr>
              </table>
            </div>

          </div>
        </div>
      </div>
    );
  }
}
