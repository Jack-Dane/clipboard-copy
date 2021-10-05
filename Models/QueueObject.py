
from queue import Queue


class QueueObject(Queue):

	def clear(self):
		"""
		Additional function to easily clear the queue object
		"""
		with self.mutex:
			self.queue.clear()
