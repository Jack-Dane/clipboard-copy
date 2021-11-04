
import logging

from unittest import TestCase
from unittest.mock import MagicMock, patch

from Models.ClipboardPoller import ClipboardPoller
from Models.QueueObject import QueueObject


class ClipboardPollerCheckItem(TestCase):

    def setUp(self):
        self.expected = "New Clipboard"
        self.clipboardQueue = MagicMock()
        self.clipboardPoller = ClipboardPoller(self.clipboardQueue)
        self.clipboardPoller.clipboardChange = MagicMock()

    @patch("pyperclip.paste")
    def testSame(self, pyperclipPaste):
        """
        Test to see variable doesn't change when clipboard is the same
        """
        pyperclipPaste.return_value = self.expected

        self.clipboardPoller.currentClipboardItem = self.expected
        self.clipboardPoller._checkItem()

        self.clipboardPoller.clipboardChange.assert_not_called()
        self.assertEqual(pyperclipPaste.call_count, 1)
        self.assertEqual(self.clipboardPoller.currentClipboardItem, self.expected)

    @patch("pyperclip.paste")
    def testChange(self, pyperclipPaste):
        """
        Test to see function to change current clipboard object variable
        """
        original = "Original Clipboard"

        pyperclipPaste.return_value = self.expected

        self.clipboardPoller.currentClipboardItem = original
        self.clipboardPoller._checkItem()

        self.clipboardPoller.clipboardChange.assert_called_once()
        self.assertEqual(pyperclipPaste.call_count, 1)


class ClipboardPollerAddItemToStackTest(TestCase):

    def setUp(self):
        """
        Set limit and item to add
        """
        self.itemToAdd = "New Clipboard"
        self.limit = 5
        self.clipboardQueue = MagicMock()
        self.clipboardPoller = ClipboardPoller(self.clipboardQueue)
        self.clipboardPoller.maxLength = self.limit

    def testAddItemWhenOverLimit(self):
        """
        Adding an item to the stack when over the stack limit
        """
        clipboardStackCurrent = [str(i) for i in range(self.limit)]
        clipboardStackExpected = [self.itemToAdd] + [str(i) for i in range(self.limit - 1)]

        self.clipboardPoller.clipboardStack = clipboardStackCurrent
        self.clipboardPoller.addItemToStack(self.itemToAdd)

        self.assertEqual(self.clipboardPoller.clipboardStack, clipboardStackExpected)
        self.assertEqual(len(self.clipboardPoller.clipboardStack), self.limit)

    def testAddItemWhenUnderLimit(self):
        """
        Adding an item to the stack when stack len equal to the limit
        """
        clipboardStackCurrent = [str(i) for i in range(self.limit - 1)]
        clipboardStackExpected = [self.itemToAdd] + clipboardStackCurrent

        self.clipboardPoller.clipboardStack = clipboardStackCurrent
        self.clipboardPoller.addItemToStack(self.itemToAdd)

        self.assertEqual(self.clipboardPoller.clipboardStack, clipboardStackExpected)
        self.assertEqual(len(self.clipboardPoller.clipboardStack), self.limit)

    def testAddItemWhenOverLimitMoreThanOne(self):
        """
        Adding an item when already over the limit, should reduce down to limit
        """
        clipboardStackCurrent = [str(i) for i in range(self.limit + 5)]
        clipboardStackExpected = [self.itemToAdd] + [str(i) for i in range(self.limit - 1)]

        self.clipboardPoller.clipboardStack = clipboardStackCurrent
        self.clipboardPoller.addItemToStack(self.itemToAdd)

        self.assertEqual(self.clipboardPoller.clipboardStack, clipboardStackExpected)
        self.assertEqual(len(self.clipboardPoller.clipboardStack), self.limit)


class ClipboardPollerClipboardChange(TestCase):

    @patch("logging.basicConfig")
    @patch("logging.info")
    @patch("os.makedirs")
    def setUp(self, loggingBasicConfig, loggingInfo, osMakedirs):
        self.clipboardItem = "New Clipboard"
        self.clipboardQueue = MagicMock()
        self.clipboardQueue.put = MagicMock()
        self.clipboardPoller = ClipboardPoller(self.clipboardQueue)
        self.clipboardPoller.currentClipboardItem = "Old Clipboard"
        self.clipboardPoller.addItemToStack = MagicMock()

    def testClipboardChangeWhenUsingParameterVariable(self):
        """
        Setting a new clipboard variable without providing item as parameter
        """
        self.clipboardPoller.clipboardChange(self.clipboardItem)

        self.assertEqual(self.clipboardQueue.put.call_count, 1)
        self.assertEqual(self.clipboardPoller.currentClipboardItem, self.clipboardItem)
        self.assertEqual(self.clipboardPoller.addItemToStack.call_count, 1)

    @patch("pyperclip.paste")
    def testClipboardChangeWhenUsingPyperclipPaster(self, pyperclipPaste):
        """
        Setting a new clipboard variable when providing item as parameter
        """
        pyperclipPaste.return_value = self.clipboardItem
        self.clipboardPoller.clipboardChange()

        self.assertEqual(self.clipboardQueue.put.call_count, 1)
        self.assertEqual(self.clipboardPoller.currentClipboardItem, self.clipboardItem)
        self.assertEqual(self.clipboardPoller.addItemToStack.call_count, 1)
