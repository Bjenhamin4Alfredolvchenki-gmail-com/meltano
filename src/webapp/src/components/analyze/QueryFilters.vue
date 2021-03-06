<script>
import { mapActions, mapGetters, mapState } from 'vuex'

export default {
  name: 'QueryFilters',
  data() {
    return {
      addFilterModel: {
        attributeHelper: {
          attribute: null,
          type: ''
        },
        expression: '',
        value: '',
        isActive: true
      }
    }
  },
  computed: {
    ...mapState('designs', ['filterOptions', 'filters']),
    ...mapGetters('designs', [
      'getIsDateAttribute',
      'getNonDateFilters',
      'getTableSources',
      'hasNonDateFilters'
    ]),
    getFilterInputType() {
      return filterType => (filterType === 'aggregate' ? 'number' : 'text')
    },
    getHasAtLeastOneLikeFilter() {
      const likeExpression = 'like'
      const filterModelHasLike = this.filters.find(
        filter => filter.expression === likeExpression
      )
      return (
        filterModelHasLike || this.addFilterModel.expression === likeExpression
      )
    },
    getHasMultipleFilters() {
      return this.getNonDateFilters.length > 1
    },
    getHasValidatedOptionals() {
      return (expression, value) =>
        this.getIsExpressionNullRelated(expression) || Boolean(value)
    },
    getIsExpressionNullRelated() {
      return expression =>
        expression === 'is_null' || expression === 'is_not_null'
    },
    getIsFilterValid() {
      return filter =>
        this.getHasValidatedOptionals(filter.expression, filter.value)
    },
    getSourcesWithoutDateAttributes() {
      return this.getTableSources
        ? this.getTableSources.map(source => ({
            ...source,
            columns: source.columns.filter(
              attribute => !this.getIsDateAttribute(attribute)
            )
          }))
        : []
    },
    isFirstFilterMatch() {
      return filter => {
        const firstFilter = this.getNonDateFilters.find(
          tempFilter => tempFilter.attribute.key === filter.attribute.key
        )
        return firstFilter === filter
      }
    },
    isValidAdd() {
      const vm = this.addFilterModel
      const hasRequiredValues = vm.attributeHelper.attribute && vm.expression
      const hasValidatedOptionals = this.getHasValidatedOptionals(
        vm.expression,
        vm.value
      )
      return hasRequiredValues && hasValidatedOptionals
    }
  },
  methods: {
    ...mapActions('designs', ['addFilter', 'removeFilter']),
    addNewFilter() {
      const vm = this.addFilterModel
      this.addFilter({
        attribute: vm.attributeHelper.attribute,
        filterType: vm.attributeHelper.type,
        expression: vm.expression,
        value: vm.value,
        isActive: vm.isActive
      })
      this.selectivelyClearAddFilterModel()
    },
    onChangeExpressionSelector(filter) {
      const isNullRelated = this.getIsExpressionNullRelated(filter.expression)
      if (isNullRelated) {
        filter.value = ''
      }
    },
    onChangeFilterValue(filter) {
      const hasValidatedOptionals = this.getHasValidatedOptionals(
        filter.expression,
        filter.value
      )
      filter.isActive = hasValidatedOptionals
    },
    selectivelyClearAddFilterModel() {
      this.addFilterModel.value = ''
    }
  }
}
</script>

<template>
  <div>
    <table
      class="table is-size-7 is-fullwidth is-narrow is-hoverable has-borderless-cells"
    >
      <thead>
        <tr>
          <th>
            <span>Attribute</span>
            <span
              class="icon has-text-grey-light tooltip is-tooltip-right"
              data-tooltip="The column or aggregate to filter."
            >
              <font-awesome-icon icon="info-circle"></font-awesome-icon>
            </span>
          </th>
          <th class="has-text-centered">
            <span>Operation</span>
            <span
              class="icon has-text-grey-light tooltip"
              data-tooltip="The filter expression for the selected column or aggregate."
            >
              <font-awesome-icon icon="info-circle"></font-awesome-icon>
            </span>
          </th>
          <th class="has-text-centered">
            <span>Value</span>
            <span
              class="icon has-text-grey-light tooltip"
              data-tooltip="The value to operate on when filtering."
            >
              <font-awesome-icon icon="info-circle"></font-awesome-icon>
            </span>
          </th>
          <th class="has-text-right">
            <span>Actions</span>
          </th>
        </tr>
      </thead>

      <tbody>
        <tr>
          <td>
            <p class="control is-expanded">
              <span class="select is-fullwidth is-small">
                <select v-model="addFilterModel.attributeHelper">
                  <optgroup
                    v-for="source in getSourcesWithoutDateAttributes"
                    :key="source.label"
                    :label="source.label"
                  >
                    <option disabled>Columns</option>
                    <option
                      v-for="column in source.columns"
                      :key="column.label"
                      :value="{
                        attribute: column,
                        type: 'column'
                      }"
                    >
                      {{ column.label }}
                    </option>
                    <option disabled>Aggregates</option>
                    <option
                      v-for="aggregate in source.aggregates"
                      :key="aggregate.label"
                      :value="{
                        attribute: aggregate,
                        type: 'aggregate'
                      }"
                    >
                      {{ aggregate.label }}
                    </option>
                  </optgroup>
                </select>
              </span>
            </p>
          </td>
          <td>
            <p class="control is-expanded">
              <span class="select is-fullwidth is-small">
                <select
                  v-model="addFilterModel.expression"
                  @change="onChangeExpressionSelector(addFilterModel)"
                >
                  <option
                    v-for="filterOption in filterOptions"
                    :key="filterOption.label"
                    :value="filterOption.expression"
                    >{{ filterOption.label }}</option
                  >
                </select>
              </span>
            </p>
          </td>
          <td>
            <p class="control is-expanded">
              <input
                v-model="addFilterModel.value"
                class="input is-small"
                :disabled="
                  getIsExpressionNullRelated(addFilterModel.expression)
                "
                :type="getFilterInputType(addFilterModel.attributeHelper.type)"
                placeholder="Filter value"
                @focus="$event.target.select()"
              />
            </p>
          </td>
          <td>
            <div class="control">
              <button
                class="button is-small is-fullwidth is-interactive-primary is-outlined"
                :disabled="!isValidAdd"
                @click="addNewFilter"
              >
                Add
              </button>
            </div>
          </td>
        </tr>

        <template v-if="hasNonDateFilters">
          <br />

          <tr
            v-for="(filter, index) in getNonDateFilters"
            :key="`${filter.attribute.key}-${index}`"
          >
            <td>
              <p class="is-small">
                <span v-show="index > 0"><code>AND</code> </span>
                <span v-if="isFirstFilterMatch(filter)">
                  {{ filter.attribute.label }}
                </span>
              </p>
            </td>
            <td>
              <p class="control is-expanded">
                <span class="select is-fullwidth is-small">
                  <select
                    v-model="filter.expression"
                    @change="onChangeExpressionSelector(filter)"
                  >
                    <option
                      v-for="filterOption in filterOptions"
                      :key="filterOption.label"
                      :value="filterOption.expression"
                      >{{ filterOption.label }}</option
                    >
                  </select>
                </span>
              </p>
            </td>
            <td>
              <p class="control has-icons-right is-expanded">
                <input
                  v-model="filter.value"
                  class="input is-small"
                  :class="{ 'is-danger': !getIsFilterValid(filter) }"
                  :disabled="getIsExpressionNullRelated(filter.expression)"
                  :type="getFilterInputType(filter.filterType)"
                  :placeholder="
                    getIsFilterValid(filter) ? 'Filter value' : 'Invalid value'
                  "
                  @focus="$event.target.select()"
                  @input="onChangeFilterValue(filter)"
                />
                <span class="icon is-small is-right">
                  <font-awesome-icon
                    :icon="
                      getIsFilterValid(filter)
                        ? 'check'
                        : 'exclamation-triangle'
                    "
                  ></font-awesome-icon>
                </span>
              </p>
            </td>
            <td>
              <div class="control">
                <button
                  class="button is-small is-fullwidth"
                  @click.stop="removeFilter(filter)"
                >
                  Remove
                </button>
              </div>
            </td>
          </tr>
        </template>
      </tbody>
    </table>
    <div
      v-if="getHasAtLeastOneLikeFilter || getHasMultipleFilters"
      class="content is-size-7"
    >
      <template v-if="getHasAtLeastOneLikeFilter">
        <hr class="hr-tight" />
        <p><code>LIKE</code> options:</p>
        <ul>
          <li><code>_</code>: matches any single character</li>
          <li>
            <code>%</code>: matches any sequence of zero or more characters
          </li>
        </ul>
      </template>
      <template v-if="getHasMultipleFilters">
        <hr class="hr-tight" />
        <p class="has-text-centered">
          Currently, we only have the <code>AND</code> option for filter chains;
          but we intend to support more!
        </p>
      </template>
    </div>
  </div>
</template>

<style lang="scss"></style>
