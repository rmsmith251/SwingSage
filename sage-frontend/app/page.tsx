import { LinkedinLink, GitHubLink, SubstackLink } from './common'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div><a><h1 className='{`mb-3 text-2xl font-semibold`}'>About Me</h1></a></div>
      <div>
        <a>
          <h2 className='{`mb-3 text-2xl font-semibold`}'>
            I'm a Machine Learning Engineer with a passion for edge computing.
          </h2>
          <h2 className='{`mb-3 text-2xl font-semibold`}'>
            My main hobbies are gaming, golf, and beer.
          </h2>
        </a>
      </div>
      <div></div>
      <div></div>
      <div></div>
      <div className="mb-32 grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-4 lg:text-left">
        <a href="/swingsage" className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30">
          <h2 className={`mb-3 text-2xl font-semibold`}>
            SwingSage{' '}
            <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
              -&gt;
            </span>
          </h2>
          <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
            An all-in-one golf assistant.
          </p>
        </a>
        <LinkedinLink />
        <GitHubLink />
        <SubstackLink />


        {/* <a
          href="https://vercel.com/new?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
          className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2 className={`mb-3 text-2xl font-semibold`}>
            Deploy{' '}
            <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
              -&gt;
            </span>
          </h2>
          <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
            Instantly deploy your Next.js site to a shareable URL with Vercel.
          </p>
        </a> */}
      </div>
    </main>
  )
}
