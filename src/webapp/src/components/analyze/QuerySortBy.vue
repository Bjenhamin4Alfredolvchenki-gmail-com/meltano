<script>
import { mapActions, mapGetters, mapState } from 'vuex'

import draggable from 'vuedraggable'

export default {
  name: 'QuerySortBy',
  components: {
    draggable
  },
  computed: {
    ...mapState('designs', ['order']),
    ...mapGetters('designs', ['getIsOrderableAttributeAscending']),
    draggableOptions() {
      return {
        animation: 100,
        emptyInsertThreshold: 30,
        ghostClass: 'drag-ghost',
        group: 'sortBy'
      }
    }
  },
  methods: {
    ...mapActions('designs', [
      'resetSortAttributes',
      'runQuery',
      'updateSortAttribute'
    ])
  }
}
</script>

<template>
  <div>
    <div class="dropdown-item">
      <draggable
        v-model="order.unassigned"
        v-bind="draggableOptions"
        class="drag-list is-flex is-flex-column has-background-white-bis"
        @end="runQuery"
      >
        <transition-group>
          <div
            v-for="orderable in order.unassigned"
            :key="`${orderable.sourceName}-${orderable.attributeName}`"
            class="drag-list-item has-background-white"
          >
            <div class="drag-handle has-text-weight-normal">
              <span class="icon is-small">
                <font-awesome-icon icon="arrows-alt-v"></font-awesome-icon>
              </span>
              <span>{{ orderable.attributeLabel }}</span>
            </div>
          </div>
        </transition-group>
      </draggable>

      <div
        v-if="order.unassigned.length === 0"
        class="drag-list-item drag-target-description"
      >
        <div class="drag-handle">
          <span class="icon is-small has-text-grey-light">
            <font-awesome-icon icon="arrows-alt-v"></font-awesome-icon>
          </span>
          <span class="is-italic is-size-7 has-text-weight-normal"
            >Drag & drop here</span
          >
        </div>
      </div>
    </div>
    <hr class="dropdown-divider" />
    <div class="dropdown-item">
      <draggable
        v-model="order.assigned"
        v-bind="draggableOptions"
        class="drag-list is-flex is-flex-column has-background-white-bis"
        @end="runQuery"
      >
        <transition-group>
          <div
            v-for="(orderable, idx) in order.assigned"
            :key="`${orderable.sourceName}-${orderable.attributeName}`"
            class="drag-list-item has-background-white has-text-interactive-secondary"
          >
            <div class="drag-handle has-text-weight-normal">
              <span class="icon is-small">
                <font-awesome-icon icon="arrows-alt-v"></font-awesome-icon>
              </span>
              <span>{{ idx + 1 }}. {{ orderable.attributeLabel }}</span>
            </div>
            <button
              class="button is-small"
              @click="updateSortAttribute(orderable)"
            >
              <span class="icon is-small has-text-interactive-secondary">
                <font-awesome-icon
                  :icon="
                    getIsOrderableAttributeAscending(orderable)
                      ? 'sort-amount-down'
                      : 'sort-amount-up'
                  "
                ></font-awesome-icon>
              </span>
            </button>
          </div>
        </transition-group>
      </draggable>

      <div
        v-if="order.assigned.length === 0"
        class="drag-list-item drag-target-description"
      >
        <div class="drag-handle">
          <span class="icon is-small has-text-grey-light">
            <font-awesome-icon icon="arrows-alt-v"></font-awesome-icon>
          </span>
          <span class="is-italic is-size-7 has-text-weight-normal"
            >Drag & drop here</span
          >
        </div>
      </div>
    </div>
    <template v-if="order.assigned.length > 0">
      <hr class="dropdown-divider" />
      <div class="dropdown-item">
        <a
          class="button is-small is-block has-text-weight-normal"
          @click.stop="resetSortAttributes"
          >Reset</a
        >
      </div>
    </template>
  </div>
</template>

<style lang="scss">
.drag-list {
  min-height: 32px;
}
.drag-list-item {
  display: flex;
  align-items: center;
  margin: 0.25rem;
  padding: 0.25rem;

  &.drag-target-description {
    position: absolute;
    left: 0;
    top: 0;
    padding: 6px 1.25rem;

    .drag-handle {
      cursor: default;
    }
  }

  .drag-handle {
    display: flex;
    flex-direction: row;
    align-items: center;
    flex-grow: 1;
    cursor: grab;
    padding-left: 0.25rem;

    .icon {
      align-self: flex-start;
      justify-self: flex-start;
      margin: 0.25rem 0.5rem 0.25rem 0;
    }
  }

  .button {
    align-self: flex-start;
    margin-left: 0.25rem;
  }
}
.drag-ghost {
  opacity: 0;
}
</style>