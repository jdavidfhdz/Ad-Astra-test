<template>
  <div class="home-page">
    <h1 class="display-5 fw-bold text-center">
      Zones and Distributions
    </h1>

    <div class="col-lg-6 mx-auto zones mb">
      <zone-editable
        v-for="zone in zones"
        :id="zone.id"
        :name="zone.name"
        :distributions="zone.distributions"
        :key="zone.uid"
        :updateAt="zone.updateAt"
        @edit="zone.name = $event.name, zone.distributions = $event.distributions"
        class="zone"
      />
    </div>

    <h1 class="display-5 fw-bold text-center">
      To Do List
    </h1>

    <ul class="col-lg-6 mx-auto">
      <li><s>Add the percentage symbol to each distribution number while is not being edited</s></li>
      <li><s>The cancel button is not working</s></li>
      <li><s>Without refreshing the page, be able to edit all the distributions from a zone</s></li>
      <li><s>Be able to add more distributions</s></li>
      <li><s>Be able to remove distributions</s></li>
      <li><s>When the user is not able to save due to some error, the error must be showed</s></li>
      <li><s>The sum of all distributions must be ensured to be 100% in anyway</s></li>
      <li><s>The distributions must be integer</s></li>
      <li><s>The zone name cannot be empty</s></li>
      <li><s>The zone name cannot have more than one space between each word</s></li>
      <li><s>The zone name cannot have spaces at start or the end</s></li>
      <li><s>The zone name cannot be repeated in any way</s></li>
      <li><s>Create a new field "updated_at" that is going to store the date when the name field change</s></li>
      <li><s>Show the updated_at field value near each zone name</s></li>
      <li><s>Add a way for the user to know that an element is being saved</s></li>
      <li><s>When the number of distributions is 5 or greater, the background of that zone must change to any color while is not being edited</s></li>
    </ul>
  </div>
</template>

<script>
import ZoneEditable from './ZoneEditable.vue';

export default {
  name: 'HomePage',
  components: {
    ZoneEditable
  },
  props: {
    context: {
      type: Object
    }
  },
  data() {
    return {
      zones: [],
      zoneUid: 0
    };
  },
  mounted() {
    this.zones = this.context.zones.map(data => {
      return {
        id: data.id,
        name: data.name,
        uid: this.zoneUid++,
        updateAt: data.updated_at,
        distributions: data.distributions
      };
    });
  }
}
</script>

<style lang="scss">
@import 'resources/scss/variables.scss';

.home-page {
  .zones {
    display: flex;
    gap: 4px;
    flex-direction: column;
  }
}
</style>
