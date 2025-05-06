import type { Meta, StoryObj } from "@storybook/react";
import { DateTime } from "luxon";

import DecoratoGantt from "../utils/stories/decorators/Gantt";
import { generateStoryData } from "../utils/stories/utils";

import data from "./mock.json";
import KonvaTimeline from ".";

const meta = {
  title: "Scenario/MandarinGantt",
  component: KonvaTimeline,
  decorators: [DecoratoGantt],
  tags: ["autodocs"],
  argTypes: {
    onTaskClick: {
      type: "function",
    },
    onTaskChange: {
      type: "function",
    },
  },
} satisfies Meta<typeof KonvaTimeline>;

export default meta;
type Story = StoryObj<typeof meta>;

const { resources } = generateStoryData({
  averageTaskDurationInMinutes: 200,
  resourcesCount: 3,
  tasksCount: 5,
  timeRangeInDays: 1,
});

export const Line: Story = {
  args: {
    debug: true,
    enableDrag: true,
    enableResize: true,
    onAreaSelect: undefined,
    resources,
    localized: {
      start: 'Н',
      end: 'К',
      duration: 'Д',
      completed: 'З'
    },
    resolution: "1day",
    enableLines: true,
    toolTip: true,
    displayTasksLabel: true,
    onTaskClick: (task) => task,
    initialDateTime: undefined,
    range: {
      start: "2025-03-25T00:00:00+03:00",
      end: "2025-04-13T23:59:59+03:00",
    },
    workIntervals: data,
    isoNow: '2025-03-04T10:00:00+03:00',
    tasks: [
      {
        id: "1",
        label: "Полностью 1 день",
        resourceId: "1",
        time: {
          start: "2025-03-28T09:00:00+03:00",
          end: "2025-04-01T10:54:00+03:00",
        },
        deadline: "2025-03-29T00:00:00+03:00",
      },
      {
        id: "2",
        label: "Часть одного дня",
        resourceId: "2",
        time: {
          start: "2025-04-03T09:30:00+03:00",
          end: "2025-04-03T12:00:00+03:00",
        },
        deadline: "2025-04-04T00:00:00+03:00",
      },
      {
        id: "3",
        label: "C одного дня на другой",
        resourceId: "2",
        time: {
          start: "2025-04-03T12:00:00+03:00",
          end: "2025-04-04T10:15:00+03:00",
        },
        deadline: DateTime.fromISO("2025-03-29T00:00:00+03:00").toMillis(),
      },
      {
        id: "4",
        label: "РА-00000979",
        description: 'Бехтер Илья Валерьевич Бехтер Илья Валерьевич',
        resourceId: "1",
        time: {
          start: "2025-04-02T09:00:00+03:00",
          end: "2025-04-02T18:00:00+03:00",
        },
        deadline: "2025-04-02T00:00:00+03:00",
      },
      {
        id: "5",
        label: "На 3 дня",
        resourceId: "3",
        time: {
          start: "2025-04-02T09:00:00+03:00",
          end: "2025-04-04T18:00:00+03:00",
        },
        deadline: DateTime.fromISO("2025-03-29T00:00:00+03:00").toMillis(),
      },
    ],
    onTaskChange: (task, opts) => {
      task.id, opts;
    },
  },
};
