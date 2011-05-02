#!/usr/bin/python
import os, sys
import argparse
import Image


"""
9 Patcher
Version 0.9 - Mon 2 May 2011

by Reimund Trost <reimund@code7.se>
<http://lumens.se/9patcher/>
"""
def main(argv=None):
	if argv is None:
		argv = sys.argv

	parser = argparse.ArgumentParser(description='Make 9 patch images.')
	parser.add_argument('-t', metavar='start,length', nargs='+', help='black pixels in top margin.')
	parser.add_argument('-l', metavar='start,length', nargs='+', help='black pixels in left margin.')
	parser.add_argument('-i', metavar='input', required=True, help='input graphic file')
	parser.add_argument('-o', metavar='output', help='output graphic file')

	args = vars(parser.parse_args())

	if (args['t'] == None and args['l'] == None):
		print 'No patches defined. There\'s nothing for me to do.'
	else:
		make_nine_patch(args)


def prepare_graphic(im, top, left):
	
	(width, height) = im.size
	offset_y = 1 if top != None else 0
	offset_x = 1 if left != None else 0

	prepared = Image.new('RGBA', (width + offset_x, height + offset_y), (255,255,255,255))
	prepared.paste(im, (offset_x, offset_y))
	return prepared


def make_nine_patch(args):
	outfile = ''

	if (args['o'] == None):
		base, ext = os.path.splitext(args['i'])
		outfile = ''.join([base, '.9', ext])
	else:
		outfile = args['o']

	pixels = []
	size = ()

	try:
		im = Image.open(args['i'], 'r')
		size = im.size
		out_im = prepare_graphic(im, args['t'], args['l'])
		pixels = out_im.load()
	except IOError:
		print ''.join(['Could not read ', infile, '.']) 
		return

	if args['t'] != None:
		for patch in args['t']:
			try:
				(position,length) = patch.split(',')
				for x in range(int(position), int(length) + 1):
					pixels[x + 1, 0] = (0, 0, 0, 255)
			except ValueError:
				print 'Patch regions must be specified as integer pairs.'
				return
			except IndexError:
				print ''.join(['A top patch region exceeds the image dimensions. Top patches must be within the range 0-', str(size[0] - 1), '.'])
				return
	
	if args['l'] != None:
		for patch in args['l']:
			try:
				(position,length) = patch.split(',')
				for y in range(int(position), int(length) + 1):
					pixels[0, y + 1] = (0, 0, 0, 255)
			except ValueError:
				print 'Patch regions must be specified as integer pairs.'
				return
			except IndexError:
				print ''.join(['A left patch region exceeds the image dimensions. Left paches must be within the range 0-', str(size[1] - 1), '.'])
				return

	try: 
		out_im.save(outfile, 'png')
	except IOError:
		print 'Could not create output file.'

if __name__ == "__main__":
    sys.exit(main())

