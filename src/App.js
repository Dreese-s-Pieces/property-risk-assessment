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
        predicted_zip_dmg: 0,
        predicted_total: 0,
        top_regional_offenses: [['', 0, 0], ['', 0, 0], ['', 0, 0]],
        deviation: '',
        probability: '',
        aqi: ''
      },
      loading: false,
      predicted_dmg: true
    };


  }

  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  } 

  handleSubmit(event) {
    event.preventDefault();

    this.setState({loading: true});
    let url = '/data?state=' + this.state.state + '&zip=' + this.state.zip_code + '&city=' + this.state.city


    fetch(url).then(res => res.json()).then(data => {
      console.log(data);
      this.setState({result: data})

      if (this.state.predicted_dmg < 0) {
        this.setState({predicted_dmg: false})
      }

    }).finally(() => {
      this.setState({loading: false});
    });


  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          OmniscNet: Property Risk Assessment
        </header>
        <div className='row-container'>
          <div className='address-form'>
            <h3>Search by Address</h3>
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
            <input className="address-input button"
              type="submit" 
              value="Submit"
            />
            </form>

            {this.state.loading && <div className="loader"></div>}
{/* Uncomment and use this to style loading spinner            
            {!this.state.loading && <div className="loader"></div>} */}

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
                  <td className="table-label">Total Damage for Zip Code {this.state.zip_code}:</td>
                  <td className="table-data">${this.state.result.total_dmg_for_zip.toFixed(2)}</td>
                </tr>
                <tr>
                  <td className="table-label">Total Damage for State {this.state.state}:</td>
                  <td className="table-data">${this.state.result.total_dmg_for_state.toFixed(2)}</td>
                </tr>
                {/* <tr>
                  <td className="table-label">Total Damage:</td>
                  <td className="table-data">${this.state.result.total_dmg.toFixed(2)}</td>
                </tr> */}
                <tr>
                  <td className="table-label">Zip Code Percentage of State {this.state.state} Damage:</td>
                  <td className="table-data">{this.state.result.prop_zip_dmg_for_state * 100}%</td>
                </tr>
                <tr>
                  <td className="table-label">State Percentage of Nation Damage:</td>
                  <td className="table-data">{this.state.result.prop_zip_dmg_for_nation * 100}%</td>
                </tr>
              </table>
              <p>*Damage since 2013</p>
            </div>
            <hr/>

            <div>
              <h3>Predicted Metrics</h3>
              <table>
                <tr>
                  <td className="table-label">Weather Damage for Zip Code {this.state.zip_code}:</td>
                  <td className="table-data">${this.state.result.predicted_zip_dmg.toFixed(2)}</td>
              <td className="table-data">{this.state.predicted_dmg && <span>&uarr;</span>}{!this.state.predicted_dmg && <span>&darr;</span>}</td>
                </tr>
              </table>
            </div>

            <hr/>
            <div>
            <h3>Most Common Crimes for Region {this.state.result.region}</h3>
              <table className="crime-table">
                <tr>
                  <th>Position</th>
                  <th>Type of Crime</th>
                  <th>Percentage of Crimes in Region {this.state.result.region}</th>
                  <th>Percentage of Type of Crime in Nation</th>
                </tr>
                <tr>
                  <td>1</td>
                  <td>{this.state.result.top_regional_offenses[0][0]}</td>
                  <td>{this.state.result.top_regional_offenses[0][1].toFixed(2)}%</td>
                  <td>{this.state.result.top_regional_offenses[0][2].toFixed(2)}%</td>
                </tr>
                <tr>
                  <td>2</td>
                  <td>{this.state.result.top_regional_offenses[1][0]}</td>
                  <td>{this.state.result.top_regional_offenses[1][1].toFixed(2)}%</td>
                  <td>{this.state.result.top_regional_offenses[1][2].toFixed(2)}%</td>
                </tr>
                <tr>
                  <td>3</td>
                  <td>{this.state.result.top_regional_offenses[2][0]}</td>
                  <td>{this.state.result.top_regional_offenses[2][1].toFixed(2)}%</td>
                  <td>{this.state.result.top_regional_offenses[2][2].toFixed(2)}%</td>
                </tr>
              </table>
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
                  <td className="table-data">{1 - this.state.result.probability}</td>
                </tr>
                <tr>
                  <td className="table-label">Air Quality Index:</td>
                  <td className="table-data">{this.state.result.aqi}</td>
                </tr>
              </table>
            </div>

          </div>
        </div>
      </div>
    );
  }
}
