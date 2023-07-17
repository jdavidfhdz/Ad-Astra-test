<template>
  <div class="zone-editable" :style="{ backgroundColor: shouldChangeBackgroundColor ? '#ffffd4' : 'transparent' }">
    <div
      v-if="display"
      class="zone-display"
      
    >
      <div>
        Zone Name: <strong>{{ name }}</strong> <span class="last-updated">(Last updated date: {{ updateAt }})</span> Distributions: {{ distributionDisplay }}
      </div>

      <button
        class="btn btn-primary"
        @click="setDisplay(false)"
        :disabled="saving"
      >
        Edit
      </button>
    </div>
    <div
      v-else
      class="zone-edit"
    >
      <label class="control-label">
        Zone Name
      </label>

      <input
        v-model="form.name"
        placeholder="Zone name"
        class="form-control"
        :disabled="saving"
      >

      <div class="zone-edit-distributions">
        <div v-for="(distribution, index) in form.distributions" :key="distribution.id">
          <label class="control-label">
            Distribution
          </label>
          <div class="form-control-box">
            <input
            v-model="distribution.percentage"
            placeholder="Percentage"
            class="form-control"
            type="number"
          >
            <button @click="removeDistribution(index)" class="remove-button">Remove</button>
          </div>          
        </div>
        <button @click="addDistribution" class="add-button">Add Distribution</button>
      </div>
      <p v-if="displayError" class="invalid-feedback" >{{ error }}</p>
      <div class="zone-edit-actions">
        <button
          class="btn btn-secondary"
          :disabled="saving"
          @click="cancel"
        >
         Cancel
        </button>

        <button
          class="btn btn-success"
          @click="save"
          :disabled="saving"
        >
          Save
        </button>
        
      </div>
    </div>

    <!-- Show a loading spinner -->
  <div class="loading-spinner" v-if="saving" >
    <div class="spinner"></div>
  </div>

  <div class="message-success" v-if="isDivVisible">
    <p>
      Element saved successfully
    </p>
  </div>
  </div>
  
</template>

<script>
export default {
  name: 'ZoneEditable',
  props: {
    name: String,
    updateAt: String,
    id: Number,
    distributions: Array,
  },
  data() {
    return {
      display: true,
      displayError: false,
      error: '',
      isBeingEdited: false,
      isDivVisible: false,
      form: {
        name: '',
        distributions: [],
      },
      saving: false,
    };
  },
  computed: {
    distributionDisplay() {
      return this.distributions.map(distribution => distribution.percentage + "%").join('-');
    },
    shouldChangeBackgroundColor() {
      return this.distributions.length >= 5 && !this.isBeingEdited;
    }
  },
  mounted() {
    this.getValuesFromProps();
  },
  methods: {
    getValuesFromProps() {
      this.form.name = this.name;
      this.form.distributions = this.distributions.map(distribution => {
        return {
          id: distribution.id,
          percentage: distribution.percentage
        };
      });
    },
    addDistribution() {
      this.form.distributions.push({ id: this.nextDistributionId, percentage: 0 });
      this.nextDistributionId++;
    },
    removeDistribution(index) {
      this.form.distributions.splice(index, 1);
    },
    isZoneNameValid(){
      
      const zoneName = this.form.name
      if (!zoneName.trim()) {
        this.error = "Zone Name cannot be empty!"
        return false; // Zone name is empty or only contains whitespace
      }

      if (/\s{2,}/.test(zoneName)) {
        this.error = "Zone Name cannot have more than one space between each word!"
        return false; // Zone name has more than one space between words
      }

      if (/^\s|\s$/.test(zoneName)) {
        this.error = "Zone Name cannot have spaces at start or the end!"
        return false; // Zone name has spaces at the start or the end
      }

      // Zone name cannot be repeated in any way
      const words = zoneName.trim().split(/\s+/);
      const uniqueWords = new Set(words);
      if (words.length !== uniqueWords.size) {
        this.error = "Zone Name cannot be repeated in any way!"
        return false; // Zone name has repeated words
      }

      return true; // Zone name is valid
    },
    validateDistributions() {
      
      const distributions = this.form.distributions;
      let numError = 0;
      const integerRegex  = /^-?\d+$/;
      for (const distribution of distributions) {
        if(!integerRegex.test(distribution.percentage)) numError++;
      }
      if(numError > 0){
        this.error = "The distribution must be integer!"
        return false;
      }

      if(distributions.reduce((sum, distribution) => sum + parseInt(distribution.percentage), 0) !== 100){
        this.error = "The sum of all distributions must be ensured to be 100% in anyway"
        return false;
      }

      return true; // Distributions are valid
      
    },
    setDisplay(value) {
      this.display = value;
      this.isBeingEdited = true;
      if(!this.display) {
        this.getValuesFromProps();
      }
    },
    async save() {
      this.saving = true;

      const params = {
        id: this.id,
        name: this.form.name.trim(),
        distributions: this.form.distributions
      };

      if (!this.isZoneNameValid()){
        this.displayError = true;
        this.saving = false;
        return;
      }

      if(!this.validateDistributions()){
        this.displayError = true;
        this.saving = false;
        return;
      }
        
      this.displayError = false;
      
      try {
        await axios.post('/api/zones/edit', params);
        this.isDivVisible = true; // Set the visibility of the div to true
      } catch (error) {
        this.error = error.response.data;
        this.displayError = true;
        this.saving = false;
        return;
      }   

      this.$emit('edit', {name: params.name, distributions: params.distributions});
      
      this.saving = false;
      this.display = true;
      this.isBeingEdited = false;

      

      setTimeout(() => {
        this.isDivVisible = false; // Set the visibility of the div to false after 3 seconds
      }, 1500);
    },
    cancel() {
      this.saving = false;
      this.display = true;
      this.isBeingEdited = false;
    }
  }
}
</script>

<style lang="scss">
@import 'resources/scss/variables.scss';

.zone-editable {
  border: 1px solid $gray-color;
  padding: $qmb;
  border-radius: $border-radius;

  .zone-display {
    display: flex;
    align-items: center;
    justify-content: space-between;

    .last-updated {
      font-size: 14px;
      color: #888; /* Adjust color as needed */
      margin-top: 10px; /* Add margin-top to create spacing from previous elements */
    }
  }

  .zone-edit {
    display: flex;
    flex-direction: column;
    gap: $small-action-space;

    .zone-edit-actions {
      display: flex;
      gap: $small-action-space;
      justify-content: end;
    }

    .zone-edit-distributions {
      display: grid;
      grid-template-columns: repeat(1, 1fr);
      gap: $small-action-space;

      .form-control-box{
        display: flex;

        .form-control{
          margin-right: 10px;
        }
      }
    }

    .invalid-feedback {
      display: block;
      width: 100%;
      margin-top: .25rem;
      font-size: .875em;
      color: #dc3545;
    }

    .remove-button,
    .add-button {
      padding: 8px 16px;
      background-color: #f44336;
      color: #fff;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-size: 16px;
      transition: all 0.5s;
    }

    .add-button{
      background-color: #7a7a7a;
    }

    .remove-button:hover{
      background-color: #d32f2f;
    }

    .add-button:hover {
      background-color: #555555;
    }

    .remove-button:focus{
      outline: none;
      box-shadow: 0 0 0 2px #f44336;
    }

    .add-button:focus {
      outline: none;
      box-shadow: 0 0 0 2px #7a7a7a;
    }

  }
}

.loading-spinner{
  width: 100%;
  height: 100vh;
  background-color: rgba($color: #000000, $alpha: 0.2);
  position: fixed;
  left: 0;
  top: 0;
  overflow: hidden;
  display: grid;
  justify-content: center;
  align-items: center;

  .spinner{
    border: 4px solid #f3f3f3; /* Light gray border */
    border-top: 4px solid #3498db; /* Blue border */
    border-radius: 50%;
    width: 24px;
    height: 24px;
    animation: spin 1s linear infinite; /* Rotate animation */
  }
}

.message-success{
  background-color: #fff;
  border: 1px solid #78ff7a;
  position: fixed;
  top:0;
  left: 50%;
  transform: translate(-50%, 0%);
  padding: 10px 50px;

  p{
    margin: 0;
    color: #0c450c;
    font-weight: bolder;
  }

}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
